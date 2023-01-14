from smb3_eh_manip.util import wpipe


class LivesplitWpipe:
    def __init__(self):
        self.client = wpipe.Client("LiveSplit", wpipe.Mode.Writer)
        self.client.write("startorsplit")

    def close(self):
        self.client.close()


if __name__ == "__main__":
    livesplit_wpipe = LivesplitWpipe()
    from time import sleep

    sleep(1)
    livesplit_wpipe.close()
