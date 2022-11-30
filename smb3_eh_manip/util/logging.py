import logging

from smb3_eh_manip.util import settings


def initialize_logging():
    # set up logging to file
    logging.basicConfig(
        filename="smb3_eh_manip.log",
        level=settings.get("file_log_level", fallback="INFO"),
        format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(
        settings.get("console_log_level", fallback="INFO"),
    )
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger("").addHandler(console)
