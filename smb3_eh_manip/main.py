import logging

from pyscreeze import (
    _locateAll_opencv as locate_all_opencv_pyscreeze,
    _locateAll_python as locate_all_python,
)
from timeit import default_timer as timer
import cv2
import pyautogui
import numpy as np


def main():
    initialize_logging()
    compute()


def compute_opencv_old():
    template = cv2.imread("data/smb3Frame106.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # frame_target_height = template.shape[0]
    # frame_target_width = 360  # int(frame_target_height * 16.0 / 9.0)
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
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.resize(frame, (frame_target_width, frame_target_height))
        match_probability = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF)
        # match_locations = np.where(match_probability >= 0.8)
        # match_location = np.unravel_index(match_probability.argmax(), match_probability.shape)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_probability)
        if max_val > 0.3:
            height, width = template.shape[:2]
            top_left = max_loc
            bottom_right = (top_left[0] + width, top_left[1] + height)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 5)
            cv2.putText(
                frame,
                f"max_val {max_val}",
                (50, 50),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 0, 255),
            )
        cv2.imshow("frame", frame)
        cv2.imshow("grayscale_template", template)
        cv2.waitKey(1)
    end = timer()
    cap.release()
    cv2.destroyAllWindows()
    buttonx = -1
    buttony = -1
    logging.info(f"x {buttonx} y {buttony} duration {((end-start)/iterations)}s")


def compute_opencv(grayscale=False):
    template = cv2.imread("data/smb3OpencvFrame.png")
    if grayscale:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
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
        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = list(locate_all_opencv(template, frame))
        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
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


def compute_opencv_pyscreeze_opencv(rescale=True):
    template = cv2.imread("data/smb3Frame106.png")
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


def compute_opencv_pyscreeze_python():
    template = cv2.imread("data/smb3Frame106.png")
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
        results = list(locate_all_python(template, frame))
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


def compute_pyautogui():
    start = timer()
    result = None
    i = 0
    iterations = 10
    while i != iterations:
        result = pyautogui.locateCenterOnScreen("data/smb3Frame106.png")
        i += 1
    if result:
        buttonx, buttony = result
    else:
        buttonx = -1
        buttony = -1
    end = timer()
    logging.info(f"x {buttonx} y {buttony} duration {(end-start)/iterations}s")
    return buttonx, buttony


compute = compute_opencv


def locate_all_opencv(
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


def initialize_logging():
    # set up logging to file
    logging.basicConfig(
        filename="smb3_eh_manip.log",
        level=logging.INFO,
        format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger("").addHandler(console)


if __name__ == "__main__":
    main()