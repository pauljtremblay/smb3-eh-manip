import logging

import cv2
import numpy as np

from smb3_eh_manip.ehvideo import EHVideo

RESET_FRAME_IMAGE_PATH = "data/everdriveReset.png"
START_FRAME_IMAGE_PATH = "data/smb3OpencvFrame.png"


class OpencvComputer:
    def compute(self, video_capture_source=2):
        self.ehvideo = EHVideo()
        self.ehvideo.reset()
        reset_template = cv2.imread(RESET_FRAME_IMAGE_PATH)
        template = cv2.imread(START_FRAME_IMAGE_PATH)
        cap = cv2.VideoCapture(video_capture_source)
        if not cap.isOpened():
            logging.info("Cannot open camera")
            exit()
        i = 0
        while True:
            i += 1
            ret, frame = cap.read()
            if not ret:
                logging.info("Can't receive frame (stream end?). Exiting ...")
                break
            if self.ehvideo.playing and list(
                OpencvComputer.locate_all_opencv(reset_template, frame)
            ):
                self.ehvideo.reset()
                logging.info(f"Detected reset")
            if not self.ehvideo.playing:
                results = list(OpencvComputer.locate_all_opencv(template, frame))
                for x, y, needleWidth, needleHeight in results:
                    top_left = (x, y)
                    bottom_right = (x + needleWidth, y + needleHeight)
                    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 5)
                if results:
                    self.ehvideo.reset()
                    self.ehvideo.set_playing(True)
                    logging.info(f"Detected start frame")
            cv2.imshow("frame", frame)
            self.ehvideo.render()
            cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()

    @classmethod
    def locate_all_opencv(
        cls,
        needleImage,
        haystackImage,
        limit=10000,
        region=None,
        step=1,
        confidence=0.999,
    ):
        """
        TODO - rewrite this
            faster but more memory-intensive than pure python
            step 2 skips every other row and column = ~3x faster but prone to miss;
                to compensate, the algorithm automatically reduces the confidence
                threshold by 5% (which helps but will not avoid all misses).
            limitations:
            - OpenCV 3.x & python 3.x not tested
            - RGBA images are treated as RBG (ignores alpha channel)
        """

        confidence = float(confidence)

        needleHeight, needleWidth = needleImage.shape[:2]

        if region:
            haystackImage = haystackImage[
                region[1] : region[1] + region[3], region[0] : region[0] + region[2]
            ]
        else:
            region = (0, 0)  # full image; these values used in the yield statement
        if (
            haystackImage.shape[0] < needleImage.shape[0]
            or haystackImage.shape[1] < needleImage.shape[1]
        ):
            # avoid semi-cryptic OpenCV error below if bad size
            raise ValueError(
                "needle dimension(s) exceed the haystack image or region dimensions"
            )

        if step == 2:
            confidence *= 0.95
            needleImage = needleImage[::step, ::step]
            haystackImage = haystackImage[::step, ::step]
        else:
            step = 1

        # get all matches at once, credit: https://stackoverflow.com/questions/7670112/finding-a-subimage-inside-a-numpy-image/9253805#9253805
        result = cv2.matchTemplate(haystackImage, needleImage, cv2.TM_CCOEFF_NORMED)
        match_indices = np.arange(result.size)[(result > confidence).flatten()]
        matches = np.unravel_index(match_indices[:limit], result.shape)

        if len(matches[0]) == 0:
            return

        # use a generator for API consistency:
        matchx = matches[1] * step + region[0]  # vectorized
        matchy = matches[0] * step + region[1]
        for x, y in zip(matchx, matchy):
            yield (x, y, needleWidth, needleHeight)
