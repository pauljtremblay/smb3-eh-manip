import logging

from timeit import default_timer as timer
import cv2

from pyscreeze import (
    _locateAll_opencv as locate_all_opencv_pyscreeze,
)


class PyscreezeOpencvComputer:
    def compute(rescale=True):
        template = cv2.imread("data/smb3FceuxFrame106.png")
        frame_target_height = template.shape[0]
        frame_target_width = 346  # int(frame_target_height * 16.0 / 9.0)
        cap = cv2.VideoCapture(2)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        i = 0
        iterations = 100000
        start = timer()
        while i != iterations:
            i += 1
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            if rescale:
                frame = cv2.resize(frame, (frame_target_width, frame_target_height))
            results = list(locate_all_opencv_pyscreeze(template, frame, confidence=0.3))
            for x, y, needleWidth, needleHeight in results:
                top_left = (x, y)
                bottom_right = (x + needleWidth, y + needleHeight)
                cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 5)
            cv2.imshow("frame", frame)
            cv2.imshow("grayscale_template", template)
            cv2.waitKey(1)
        end = timer()
        cap.release()
        cv2.destroyAllWindows()
        buttonx = -1
        buttony = -1
        logging.info(f"x {buttonx} y {buttony} duration {((end-start)/iterations)}s")