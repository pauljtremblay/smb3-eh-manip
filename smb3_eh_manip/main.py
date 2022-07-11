import logging

from timeit import default_timer as timer
import cv2
import pyautogui
import numpy as np


def main():
    initialize_logging()
    compute()


def compute_opencv():
    # image = pyautogui.screenshot()
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # cv2.imshow("Test", img)
    template = cv2.imread("data/smb3Frame106.png")
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    i = 0
    iterations = 100
    start = timer()
    while i != iterations:
        i += 1
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        breakpoint()
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        height, width = template.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 5)
        cv2.imshow("test", frame)
        cv2.waitKey(0)
        # cv2.imshow("frame", frame)
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break
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