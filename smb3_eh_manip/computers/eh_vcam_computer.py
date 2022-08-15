import logging
import sys

import cv2

from smb3_eh_manip.settings import config
from smb3_eh_manip.computers.opencv_computer import OpencvComputer


class EhVcamComputer:
    def __init__(self):
        self.capture = cv2.VideoCapture(config.getint("app", "video_capture_source"))
        if not self.capture.isOpened():
            logging.info("Cannot open camera")
            sys.exit()
        self.capture_template = cv2.imread("data/eh_vcam/captureTrigger.png")
        self.tas_template = cv2.imread("data/eh_vcam/tasTrigger.png")

    def tick(self):
        ret, frame = self.capture.read()
        if not ret:
            logging.warn("Can't receive frame (stream end?). Exiting ...")
            sys.exit()
        capture_results = list(
            OpencvComputer.locate_all_opencv(self.capture_template, frame)
        )
        tas_results = list(OpencvComputer.locate_all_opencv(self.tas_template, frame))

        if tas_results and capture_results:
            logging.info(f"In sync! Detected capture and TAS triggers")
        elif tas_results:
            logging.info(f"Failure! Detected TAS trigger but not capture trigger")
        elif capture_results:
            logging.info(f"Failure! Detected capture trigger but not TAS trigger")
        cv2.waitKey(1)

    def terminate(self):
        self.capture.release()
        cv2.destroyAllWindows()