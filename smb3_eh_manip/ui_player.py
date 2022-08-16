import logging

import cv2
import numpy as np

from smb3_eh_manip.settings import ACTION_FRAMES, FREQUENCY

WINDOW_TITLE = "eh manip ui"
LINE_COUNT = 6
WINDOW_SCALAR = 3
WINDOW_HEIGHT = FREQUENCY * WINDOW_SCALAR
WINDOW_WIDTH = FREQUENCY * WINDOW_SCALAR * LINE_COUNT
LINE_COLOR = (255, 255, 255)
FILL_COLOR = (128, 128, 128)
PURPLE_COLOR = (211, 0, 148)
THICKNESS = 2


class UiPlayer:
    def __init__(self):
        cv2.imshow(WINDOW_TITLE, UiPlayer.get_base_frame())

    def reset(self):
        self.trigger_frames = list(ACTION_FRAMES)

    def tick(self, current_frame):
        ui = UiPlayer.get_base_frame()
        ui = cv2.putText(
            ui,
            str(current_frame),
            (0, 32),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            FILL_COLOR,
            2,
        )
        if self.trigger_frames:
            next_trigger_distance = (
                self.trigger_frames[0] - round(current_frame)
            ) * WINDOW_SCALAR
            if next_trigger_distance < WINDOW_WIDTH:
                left_x = (
                    WINDOW_WIDTH - next_trigger_distance - 2 * FREQUENCY * WINDOW_SCALAR
                )
                start = (left_x, 0)
                end = (left_x + FREQUENCY * WINDOW_SCALAR, WINDOW_HEIGHT)
                fill_color = PURPLE_COLOR if next_trigger_distance == 0 else FILL_COLOR
                ui = cv2.rectangle(ui, start, end, fill_color, -1)
                ui = cv2.rectangle(ui, start, end, LINE_COLOR, THICKNESS)
            if self.trigger_frames[0] < current_frame - 2 * FREQUENCY:
                trigger_frame = self.trigger_frames.pop(0)
                logging.debug(
                    f"Popped trigger frame {trigger_frame} at {current_frame}"
                )
        cv2.imshow(WINDOW_TITLE, ui)

    @classmethod
    def get_base_frame(self):
        frame = np.zeros(shape=[WINDOW_HEIGHT, WINDOW_WIDTH, 3], dtype=np.uint8)
        for x in range(1, LINE_COUNT):
            frame = cv2.line(
                frame,
                (x * FREQUENCY * WINDOW_SCALAR, 0),
                (x * FREQUENCY * WINDOW_SCALAR, WINDOW_HEIGHT),
                LINE_COLOR,
                THICKNESS,
            )
        return frame