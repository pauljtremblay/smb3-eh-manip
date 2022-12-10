"""
The following dataclasses are agnostic of the underlying world and data.
Specifics like lag frames, bro indices, etc should be in their respective
modules with a specific exploit in mind (e.g. w2 is in 'eh')
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


from smb3_eh_manip.util.wizard_mixins import YAMLWizard


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    DOWN = 2
    UP = 3


@dataclass
class Level:
    name: str


@dataclass
class HammerBro:
    index: int
    item: str
    x: int
    y: int
    facing_direction: Optional[int] = 0


@dataclass
class Position:
    x: int
    y: int
    is_mushroom: bool = False
    level: Optional[Level] = None


@dataclass
class World(YAMLWizard):
    number: int
    positions: list[Position]
    hbs: list[HammerBro]

    def get_position(self, x, y):
        for position in self.positions:
            if position.x == x and position.y == y:
                return position
        return None

    def dump(self, path_prefix="data/worlds"):
        self.to_yaml_file(f"{path_prefix}/world_{self.number}.yml")

    @classmethod
    def load(cls, number, path_prefix="data/worlds"):
        return World.from_yaml_file(f"{path_prefix}/world_{number}.yml")
