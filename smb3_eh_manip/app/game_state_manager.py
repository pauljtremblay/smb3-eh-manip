from enum import Enum
import logging


class GameState(Enum):
    INITIALIZING = 1
    OVERWORLD = 2
    IN_LEVEL = 3


class GameStateManager:
    def __init__(self):
        self.reset()

    def handle_lag_frames_observed(self, observed_lag_frames):
        if GameState.INITIALIZING and observed_lag_frames == 12:
            # 12 upon entered world 1 for the first time
            self.current_state = GameState.OVERWORLD
            return
        if observed_lag_frames >= 12 and observed_lag_frames <= 13:
            self.current_state = GameState.OVERWORLD
            logging.info(f"Ended level {self.current_level}!")
            return
        if (
            observed_lag_frames >= 63 and observed_lag_frames <= 73
        ):  # 1-1 entrance is 63, 1-2 is 65?
            self.current_level += 1
            self.current_state = GameState.IN_LEVEL
            logging.info(f"Started level {self.current_level}!")
            return

    def reset(self):
        self.current_state = GameState.INITIALIZING
        self.current_level = 0
