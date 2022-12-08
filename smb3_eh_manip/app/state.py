from dataclasses import dataclass
import logging
from typing import Optional

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.nohands import NoHands
from smb3_eh_manip.util import events, settings, wizard_mixins


@dataclass
class Section:
    name: str
    lag_frames: int
    trigger: Optional[str] = None


@dataclass
class Category(wizard_mixins.YAMLWizard):
    sections: list[Section]

    @classmethod
    def load(cls, category_name=settings.get("category", fallback="nww")):
        return Category.from_yaml_file(f"data/categories/{category_name}.yml")


class State:
    def __init__(self):
        self.enable_nohands = settings.get_boolean("enable_nohands", fallback=False)
        self.nohands = NoHands() if self.enable_nohands else None
        self.reset()
        events.listen(events.LagFramesObserved, self.handle_lag_frames_observed)

    def handle_lag_frames_observed(self, event: events.LagFramesObserved):
        self.total_observed_lag_frames += event.observed_lag_frames
        self.total_observed_load_frames += event.observed_load_frames
        if not self.category.sections:
            return
        expected_lag = self.active_section().lag_frames
        if (
            expected_lag >= event.observed_load_frames - 1
            and expected_lag <= event.observed_load_frames + 1
        ):
            section = self.category.sections.pop(0)
            logging.info(f"Completed {section.name}")
            self.check_and_update_nohands(event.current_frame, section)

    def check_and_update_nohands(self, current_frame, section):
        if not self.enable_nohands or section.trigger != "nohands":
            return
        nohands_window = self.nohands.calculate_optimal_window(
            section, self.lsfr.clone()
        )
        if not nohands_window:
            return
        action_frame = round(current_frame + nohands_window.action_frame)
        events.emit(self, events.AddActionFrame(action_frame, nohands_window.window))

    def tick(self, current_frame):
        # we need to see how much time has gone by and increment RNG that amount
        lsfr_increments = (
            int(current_frame)
            - self.lsfr_frame
            - self.total_observed_lag_frames
            - self.total_observed_load_frames
        )
        self.lsfr.next_n(lsfr_increments)
        self.lsfr_frame += lsfr_increments

    def reset(self):
        self.total_observed_lag_frames = 0
        self.total_observed_load_frames = 0
        self.lsfr_frame = 12
        self.category = Category.load()
        self.lsfr = LSFR()

    def active_section(self):
        return self.category.sections[0]
