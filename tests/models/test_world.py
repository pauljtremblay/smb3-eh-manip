import unittest
import tempfile

from smb3_eh_manip.models import world as models


class TestWorld(unittest.TestCase):
    def test_serialize(self):
        world = models.World(
            number=2,
            positions=[
                models.Position(x=5, y=3, level=models.Level(name="2-3")),
                models.Position(
                    x=6,
                    y=3,
                    hammer_bro=models.HammerBro(index=2, item="box"),
                ),
                models.Position(x=7, y=3, level=models.Level(name="2-quicksand")),
                models.Position(x=7, y=4),
                models.Position(x=8, y=4, level=models.Level(name="2-4")),
                models.Position(x=9, y=4),
                models.Position(x=9, y=3),
                models.Position(
                    x=9,
                    y=2,
                    hammer_bro=models.HammerBro(index=3, item="hammer"),
                ),
            ],
        )
        world.dump(path_prefix=tempfile.tempdir)
        world_load = models.World.load(
            number=world.number, path_prefix=tempfile.tempdir
        )
        self.assertEqual(world, world_load)
