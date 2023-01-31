import logging
from multiprocessing import Process, Value
import socket
import time
import win32file, win32pipe

from smb3_eh_manip.util import events
from smb3_eh_manip.util.logging import initialize_logging


def client_process(split_index_value: Value):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 16834))
    while True:
        s.send(b"getsplitindex\r\n")
        split_index = int(s.recv(1024).decode("utf-8"))
        split_index_value.value = split_index
        time.sleep(0.2)


class LivesplitClient:
    def __init__(self):
        self.last_split_index = -1
        self.split_index_value = Value("i", self.last_split_index)
        self.process = Process(
            target=client_process,
            args=(self.split_index_value,),
        )
        self.process.daemon = True
        self.process.start()

    def initialize_named_pipe(self):
        # TODO this is preferred to tcp, but is currently not working for whatever reason.
        self.handle = win32file.CreateFile(
            r"\\.\pipe\LiveSplit",
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            win32file.FILE_ATTRIBUTE_NORMAL,
            None,
        )
        res = win32pipe.SetNamedPipeHandleState(
            self.handle, win32pipe.PIPE_READMODE_BYTE, None, None
        )
        self.handle.write("startorsplit")
        response = win32file.ReadFile(self.handle, 65536)
        print(response)

    def tick(self):
        split_index = self.split_index_value.value
        if split_index != self.last_split_index:
            logging.info(
                f"Livesplit client detected split change from {self.last_split_index} to {split_index}"
            )
            events.emit(
                self,
                events.LivesplitCurrentSplitIndexChanged(
                    split_index,
                    self.last_split_index,
                ),
            )
            self.last_split_index = split_index


if __name__ == "__main__":
    initialize_logging(
        console_log_level="DEBUG",
        file_log_level="DEBUG",
        filename="livesplit_client.log",
    )
    client = LivesplitClient()
    from time import sleep

    while True:
        client.tick()
        sleep(1)
    client.close()
