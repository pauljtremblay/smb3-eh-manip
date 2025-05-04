import logging
from multiprocessing import Process, Value
import time
import win32file, win32pipe

from smb3_eh_manip.util import events, settings
from smb3_eh_manip.util.logging import initialize_logging

LOGGER = logging.getLogger(__name__)
LIVESPLIT_REQUEST_FREQUENCY = settings.get_float(
    "livesplit_request_frequency", fallback=0.25
)

NAMED_PIPE = r"\\.\pipe\LiveSplit"


def create_named_pipe():
    try:
        return win32pipe.CreateNamedPipe(
            NAMED_PIPE,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,
            2,
            65536,
            65536,
            0,
            None
        )
    except:
        LOGGER.error("Failed to create named pipe.", exc_info=True)
        return None


def get_pipe_file_handle():
    try:
        return win32file.CreateFile(
            NAMED_PIPE,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            win32file.FILE_ATTRIBUTE_NORMAL,
            None,
        )
    except:
        LOGGER.error("Failed to get handle of named pipe.", exc_info=True)
        return None


def client_process(split_index_value: Value, do_split_value: Value):
    initialize_logging(
        console_log_level="DEBUG",
        file_log_level="DEBUG",
        filename="livesplit_client.log",
    )
    fd = create_named_pipe()
    handle = get_pipe_file_handle()
    res = win32pipe.SetNamedPipeHandleState(
         fd, win32pipe.PIPE_READMODE_BYTE, None, None
    )
    if res == 0:
        print(f"SetNamedPipeHandleState return code: {res}")
    while True:
        win32file.WriteFile(handle, b"getsplitindex\r\n")
        result, data = win32file.ReadFile(handle, 65536)
        if result == 0:
            split_index_value.value = int(data.decode("utf-8").strip())
        if do_split_value.value:
            do_split_value.value = 0
            win32file.WriteFile(handle, b"split\r\n")
            result, data = win32file.ReadFile(handle, 65536)
            LOGGER.info("Livesplit client split result: %d, data: %s", result, data)
        time.sleep(LIVESPLIT_REQUEST_FREQUENCY)


class LivesplitClient:
    def __init__(self):
        self.last_split_index = -1
        self.split_index_value = Value("i", self.last_split_index)
        self.do_split_value = Value("i", 0)
        self.process = Process(
            target=client_process,
            args=(self.split_index_value, self.do_split_value),
        )
        self.process.daemon = True
        self.process.start()

    def tick(self):
        split_index = self.split_index_value.value
        if split_index != self.last_split_index:
            LOGGER.info("Livesplit client detected split change from %d to %d",
                        self.last_split_index, split_index)
            events.emit(
                self,
                events.LivesplitCurrentSplitIndexChanged(
                    split_index,
                    self.last_split_index,
                ),
            )
            self.last_split_index = split_index

    def split(self):
        self.do_split_value.value = 1


if __name__ == "__main__":
    initialize_logging(
        console_log_level="DEBUG",
        file_log_level="DEBUG",
        filename="livesplit_client.log",
    )
    client = LivesplitClient()

    while True:
        client.tick()
        time.sleep(1)
