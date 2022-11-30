from dataclasses import dataclass
import json
from typing import Optional

from dataclass_wizard import JSONWizard


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
class World(JSONWizard):
    number: int
    positions: list[Position]

    def dump(self, path_prefix="data/worlds"):
        world_path = f"{path_prefix}/world_{self.number}.json"
        with open(world_path, "w", encoding="utf8") as json_file:
            json.dump(self.to_dict(), json_file)

    @classmethod
    def load(cls, number, path_prefix="data/worlds"):
        world_path = f"{path_prefix}/world_{number}.json"
        with open(world_path, "r", encoding="utf8") as json_file:
            return World.from_dict(json.load(json_file))
