from dataclasses import dataclass
import logging

from dataclass_wizard import YAMLWizard

from smb3_eh_manip.util import settings


@dataclass
class Section:
    name: str
    lag_frames: int


@dataclass
class Category(YAMLWizard):
    sections: list[Section]

    @classmethod
    def load(cls, category_name=settings.get("category", fallback="nww")):
        return Category.from_yaml_file(f"data/categories/{category_name}.yml")


class State:
    def __init__(self):
        self.category_name = settings.get("category", fallback="nww")
        self.reset()

    def handle_lag_frames_observed(self, observed_lag_frames, load_frames_observed):
        recent_load_frames = load_frames_observed - self.last_lag_frame_count
        if not recent_load_frames:
            return
        if not self.category.sections:
            return
        expected_lag = self.active_section().lag_frames
        if (
            expected_lag >= recent_load_frames - 1
            and expected_lag <= recent_load_frames + 1
        ):
            section = self.category.sections.pop(0)
            logging.info(f"Completed {section.name}")

    def reset(self):
        self.last_lag_frame_count = 0
        self.category = Category.load()

    def active_section(self):
        return self.category.sections[0]
