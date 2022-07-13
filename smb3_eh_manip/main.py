from smb3_eh_manip.logging import initialize_logging
from smb3_eh_manip.settings import config
from smb3_eh_manip.computers import EhComputer, CalibrationComputer, TwoOneComputer


def main():
    initialize_logging()
    if config.get("app", "computer") == "eh":
        computer = EhComputer()
    elif config.get("app", "computer") == "twoone":
        computer = TwoOneComputer()
    else:
        computer = CalibrationComputer()
    computer.compute()


if __name__ == "__main__":
    main()