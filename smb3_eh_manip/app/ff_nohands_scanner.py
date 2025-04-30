import math
import statistics
from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple

from smb3_video_autosplitter.settings import NES_FRAMERATE

from smb3_eh_manip.app.lsfr import LSFR, ITERS_FOR_ONES_BIT_PROP
from smb3_eh_manip.app.nohands import TO_HAND2_CHECK_FRAME_DURATION, TO_HAND3_CHECK_FRAME_DURATION


@dataclass
class GoodHandWindow:
    """Model that represents decent run of consecutive iterations that avoid the hand trap."""
    start_iter: int
    end_iter: int
    streak: int

    @classmethod
    def from_start_frame_and_streak(cls, start_iter: int, streak: int): return GoodHandWindow(
        start_iter=start_iter,
        end_iter=start_iter + streak - 1,
        streak=streak
    )

    def in_window(self, iteration) -> bool:
        """Is the proposed iteration within this window?"""
        return self.start_iter <= iteration <= self.end_iter

    def __str__(self):
        return f"[{self.start_iter} - {self.end_iter}]  (streak = {self.streak})"


@dataclass
class GoodHandSequence:
    """Model that represents a decent sequence of 3 good-hands streaks for potential no-hands trifectas."""
    h1_iteration: int
    h2_iteration: int
    h3_iteration: int
    h1_score: int
    h2_score: int
    h3_score: int
    mean_score: float
    std_dev: float
    good_hands_windows: List[GoodHandWindow]

    def __str__(self):
        formatted = (
            f"Iterations: {self.h1_iteration}, {self.h2_iteration}, {self.h3_iteration}\n"
            f"    Avg Score = {self.mean_score:0.2f},   Std Dev = {self.std_dev:0.3f},"
            f"   Weighted scores (H1, H2, H3) = {self.h1_score}, {self.h2_score}, {self.h3_score}\n"
        )
        for w in self.good_hands_windows:
            formatted += f"    [{w.start_iter} - {w.start_iter + w.streak - 1}]  (streak = {w.streak})\n"
        return formatted


class NoHandsScanner:
    """Utility that scans all RNG sequences for the specified amount of time, looking for optimal no-hands runs."""

    def __init__(self, *,
                 minutes_to_scan: int = 60,
                 min_consecutive_threshold: int = 3,
                 score_cap: Optional[int] = 10):
        self.min_consecutive_threshold = min_consecutive_threshold
        self.max_iteration = math.ceil(NES_FRAMERATE * 60 * minutes_to_scan)
        self.good_hands_iter_to_window: Dict[int, GoodHandWindow] = {}
        self.good_hand_streak_histogram: Dict[int, List[int]] = {}
        self.good_hand_arr: List[bool] = [
            not lsfr.hand_check()
            for i in range(self.max_iteration)
            if (lsfr:=LSFR.lsfr_from_cache(i))
        ]
        self.good_hands_weighted_score: Dict[int, int] = {}
        # build up a database on contiguous good hands iter sequences, assign weighted scores based on length of run
        self._scan_for_good_hand_windows(score_cap)

    def is_good_hand(self, iteration: int) -> bool:
        """True if this iteration is not a hand trap."""
        return self.good_hand_arr[iteration]

    def get_good_hand_window(self, iteration: int) -> Optional[GoodHandWindow]:
        """Returns the model for this streak, if and only if this iteration is part of a streak."""
        if iteration in self.good_hands_iter_to_window:
            return self.good_hands_iter_to_window[iteration]
        return None

    def show_good_hand_sequences(self) -> None:
        desc_sorted_hand_streak_histogram = dict(sorted(self.good_hand_streak_histogram.items(), reverse=True))
        print(f"\nGood hands histogram:\n")
        for (streak_length, matches) in desc_sorted_hand_streak_histogram.items():
            print(f"{streak_length} consecutive good hand iterations: {len(matches)} matches")
            if len(matches) > 1000:
                print("TOO MANY TO SHOW")
            else:
                print(", ".join([str(match) for match in matches]))
            print("")

    def scan_for_ideal_good_hand_sequences(self, *,
                                           hand_1_to_2_iterations: int = TO_HAND2_CHECK_FRAME_DURATION,
                                           hand_2_to_3_iterations: int = TO_HAND3_CHECK_FRAME_DURATION,
                                           min_score_mean: float = 6.0,
                                           max_score_std_dev: float = 5.0,
                                           only_streaks: bool = False,
                                           iter_range: Optional[Tuple[int, int]] = None) -> List[GoodHandSequence]:
        print("\nGood all no-hands sequences")
        (min_iter, max_iter) = iter_range if iter_range is not None else (0, self.max_iteration)
        good_sequences: List[GoodHandSequence] = []
        for h1_iter in range(self.max_iteration - hand_1_to_2_iterations - hand_2_to_3_iterations):
            if not min_iter <= h1_iter <= max_iter:
                continue
            h2_iter = h1_iter + TO_HAND2_CHECK_FRAME_DURATION
            h3_iter = h2_iter + TO_HAND3_CHECK_FRAME_DURATION
            # only proceed if all 3 spaced iterations are not hand traps
            if not self.is_good_hand(h1_iter) or not self.is_good_hand(h2_iter) or not self.is_good_hand(h3_iter):
                continue
            h1_score = self.good_hands_weighted_score[h1_iter]
            h2_score = self.good_hands_weighted_score[h2_iter]
            h3_score = self.good_hands_weighted_score[h3_iter]
            good_windows = [good_window
                            for iteration in [h1_iter, h2_iter, h3_iter]
                            if (good_window := self.get_good_hand_window(iteration))
                            if good_window is not None]
            if only_streaks and len(good_windows) < 3:
                continue
            mean = statistics.mean([h1_score, h2_score, h3_score])
            std_dev = statistics.stdev([h1_score, h2_score, h3_score])
            if mean >= min_score_mean and std_dev < max_score_std_dev:
                good_sequence = GoodHandSequence(h1_iteration=h1_iter,
                                                 h2_iteration=h2_iter,
                                                 h3_iteration=h3_iter,
                                                 h1_score=h1_score,
                                                 h2_score=h2_score,
                                                 h3_score=h3_score,
                                                 mean_score=mean,
                                                 std_dev=std_dev,
                                                 good_hands_windows=good_windows)
                good_sequences.append(good_sequence)
        return good_sequences

    def _scan_for_good_hand_windows(self, score_cap: Optional[int]) -> None:
        """Builds a dataset of all runs with N or more adjacent "no hands" RNG rolls."""
        good_hands_streak_iter_to_length: Dict[int, int] = {}
        for offset in range(ITERS_FOR_ONES_BIT_PROP):
            self.good_hands_weighted_score[offset] = 0
        iteration = ITERS_FOR_ONES_BIT_PROP
        num_consecutive_good = 0
        # build dataset of all runs of adjacent good hands
        while iteration < self.max_iteration:
            if self.is_good_hand(iteration):
                num_consecutive_good += 1
            else:
                if num_consecutive_good > 0:
                    # end of run: score the run, record it if within threshold
                    self._process_good_hand_window(iteration - num_consecutive_good, num_consecutive_good,
                                                   score_cap=score_cap)
                    good_hands_streak_iter_to_length[iteration] = num_consecutive_good
                num_consecutive_good = 0
            iteration += 1
        for (iteration, streak_length) in good_hands_streak_iter_to_length.items():
            if streak_length not in self.good_hand_streak_histogram.keys():
                self.good_hand_streak_histogram[streak_length] = []
            self.good_hand_streak_histogram[streak_length].append(iteration)

    def _process_good_hand_window(self, start_iter: int, streak: int, *,
                                  score_cap: Optional[int] = None) -> None:
        scores = get_pascal_row(streak, score_cap=score_cap)
        for (offset, score) in enumerate(scores):
            score_to_use = score
            self.good_hands_weighted_score[start_iter + offset] = score_to_use
        if streak >= self.min_consecutive_threshold:
            good_hand_window = GoodHandWindow.from_start_frame_and_streak(start_iter, streak)
            for offset in range(streak):
                self.good_hands_iter_to_window[start_iter + offset] = good_hand_window


def get_pascal_row(row: int, *,
                   score_cap: Optional[int] = None) -> List[int]:
    """
    Returns the last row of this pascal triangle, used for scoring good hand runs: longer streak -> higher score

    row 1:         [1]
    row 2:       [1, 1]
    row 3:     [1, 2, 1]
    row 4:   [1, 3, 3, 1]
    row 5: [1, 4, 6, 4, 1]

    So for example if a good hand window is a sequence of 5 iterations, the resulting weighted scores would be:

        1st iter in sequence: 1
        2nd iter in sequence: 4
        3rd iter in sequence: 6
        4th iter in sequence: 4
        5th iter in sequence: 1

    This algorithm scores iterations in the middle of a streak higher than iterations on the outskirts.

    If a score cap is provided, then the resulting iteration's score gets capped if the score exceeds that cap.
    """
    triangle = []
    for i in range(row):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    if score_cap is None:
        return triangle[-1]
    else:
        return [capped_score
                for raw_score in triangle[-1]
                if (capped_score:=score_cap if raw_score > score_cap else raw_score)]
