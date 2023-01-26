import socket
import win32file, win32pipe


class LivesplitClient:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("localhost", 16834))

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
        self.s.send(b"getcurrentsplitname\r\n")
        response = self.s.recv(1024).decode("utf-8")
        print(response)

    def close(self):
        self.handle.close()


if __name__ == "__main__":
    client = LivesplitClient()
    from time import sleep

    while True:
        client.tick()
        sleep(1)
    client.close()
