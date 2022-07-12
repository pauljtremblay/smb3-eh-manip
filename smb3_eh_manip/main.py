from smb3_eh_manip.logging import initialize_logging
from smb3_eh_manip.opencv_computer import OpencvComputer


def main():
    initialize_logging()
    computer = OpencvComputer()
    computer.compute()


if __name__ == "__main__":
    main()