from typing import Dict, List, Optional

INITIAL_SEED = [0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
"""This is the RNG memory's initial state after reboot"""

ITERS_FOR_ONES_BIT_PROP = 67
"""How many iterations before the lowest bit of the 8th byte is equal to 1"""

ITERS_BEFORE_DUPE = 2**15 -1
"""How many iterations before the RNG cycle begins repeating (after full propagation)"""

FIRST_DUPE_ITER = ITERS_FOR_ONES_BIT_PROP + ITERS_BEFORE_DUPE
"""The last iteration with a distinct state"""


class LSFR:

    # cache to hold all possible states from the initial seed
    # iteration to LSFR cache: iteration -> LSFR
    # LSFR to iteration cache: (18-char hex str) -> iteration
    iter_to_lsfr: Dict[int, 'LSFR'] = {}
    lsfr_to_iter: Dict[str, int] = {}

    def __init__(self, data: Optional[List[int]] = None):
        if data is not None:
            assert len(data) == 9
        self.data: List[int] = list(INITIAL_SEED) if data is None else data

    def clone(self):
        return LSFR(list(self.data))

    def get(self, byte: int) -> int:
        return self.data[byte]

    def next_n(self, iterations: int, /,
               optimize: bool = True) -> None:
        iters = self.get_effective_iteration(iterations) if optimize else iterations
        for _ in range(iters):
            self.next()

    def next(self) -> List[int]:
        temp = self.data[0] & 0x2
        carry = not not ((self.data[1] & 0x2) ^ temp)
        for i, rng_byte in enumerate(self.data):
            b = rng_byte & 1
            self.data[i] = (carry << 7) | (rng_byte >> 1)
            carry = b
        return self.data

    def random_n(self, offset: int = 0) -> int:
        # RandomN is the value most of the code uses or indexes off of.
        # It is the second byte in the array.
        # HB directions use an offset for which index they are, e.g.
        # w1 bro is index 2 so we'd look in data[1+2], or the 4th byte
        return self.data[1 + offset]

    def hand_check(self) -> bool:
        # returns True if a hand grabs the player, False otherwise
        return self.random_n() & 0x1 == 0

    @classmethod
    def for_iteration_n(cls, iteration: int):
        lsfr = LSFR()
        lsfr.next_n(iteration)
        return lsfr

    @classmethod
    def get_effective_iteration(cls, iteration: int) -> int:
        assert iteration >= 0
        if iteration < FIRST_DUPE_ITER:
            return iteration
        else:
            return iteration % ITERS_BEFORE_DUPE

    @classmethod
    def lsfr_from_cache(cls, iteration: int) -> 'LSFR':
        if len(cls.iter_to_lsfr) == 0:
            cls.initialize_lsfr_state_cache()
        return cls.iter_to_lsfr[cls.get_effective_iteration(iteration)]

    @classmethod
    def iter_from_cache(cls, lsrf_state: str | List[int]) -> Optional[int]:
        if len(cls.lsfr_to_iter) == 0:
            cls.initialize_lsfr_state_cache()
        try:
            match lsrf_state:
                case str() as byte_str:
                    key = byte_str.lower().replace(" ", "")
                case list(byte_arr):
                    key = to_hex_str(byte_arr)
                case _:
                    key = None
            return cls.lsfr_to_iter[key]
        except:
            return None

    @classmethod
    def initialize_lsfr_state_cache(cls) -> None:
        """Loads the cache of all possible RNG states, takes about 89ms on AMD Ryzen 9 5950X 16-core proc"""
        cls.iter_to_lsfr: Dict[int, LSFR] = {}
        cls.lsfr_to_iter: Dict[bytes, int] = {}

        lsfr = LSFR()
        for iteration in range(FIRST_DUPE_ITER):
            cls.iter_to_lsfr[iteration] = lsfr.clone()
            cls.lsfr_to_iter[to_hex_str(lsfr.data)] = iteration
            lsfr.next()


def to_hex_str(data: List[int]) -> str:
    # assert len(data) == 9
    # for i in range(9):
    #     assert 0 <= data[i] <= 0xff
    return "".join([f"{b:02x}" for b in data])


def from_hex_str(hex_str: str) -> List[int]:
    cleaned = hex_str.lower().replace(" ", "")
    assert len(cleaned) == 18
    return [int(f"{cleaned[i * 2]}{cleaned[1 + i * 2]}", 16) for i in range(9)]
