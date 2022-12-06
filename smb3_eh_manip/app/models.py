"""
The following dataclasses are agnostic of the underlying world and data.
Specifics like lag frames, bro indices, etc should be in their respective
modules with a specific exploit in mind (e.g. w2 is in 'eh')
"""
from dataclasses import dataclass
import json
from typing import Optional

from dataclass_wizard import YAMLWizard

BRO_MOVEMENT_FRAMES = 32  # it takes 32 frames for a HB to make 1 movement
LEVEL_FACE_TO_MOVE_FRAMES = 39
FORT_FACE_TO_MOVE_FRAMES = 102


@dataclass
class Level:
    name: str


@dataclass
class HammerBro:
    index: int
    item: str


@dataclass
class Position:
    x: int
    y: int
    is_mushroom: bool = False
    level: Optional[Level] = None
    hammer_bro: Optional[HammerBro] = None


@dataclass
class World(YAMLWizard):
    number: int
    positions: list[Position]

    def dump(self, path_prefix="data/worlds"):
        self.to_yaml_file(f"{path_prefix}/world_{self.number}.yml")

    @classmethod
    def load(cls, number, path_prefix="data/worlds"):
        return World.from_yaml_file(f"{path_prefix}/world_{number}.yml")
