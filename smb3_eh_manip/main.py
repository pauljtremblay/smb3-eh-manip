from smb3_eh_manip.logging import initialize_logging
from smb3_eh_manip.computers import EhComputer, CalibrationComputer


def main():
    initialize_logging()
    computer = EhComputer()
    computer.compute()


if __name__ == "__main__":
    main()