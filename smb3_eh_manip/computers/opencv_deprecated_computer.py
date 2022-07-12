import logging

from timeit import default_timer as timer
import cv2


class OpencvDeprecatedComputer:
    def compute():
        template = cv2.imread("data/smb3FceuxFrame106.png")
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