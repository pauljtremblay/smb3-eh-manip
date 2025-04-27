import unittest

from smb3_eh_manip.app.lsfr import LSFR, from_hex_str
from smb3_eh_manip.util.timer_tasks import timed


class TestLSFR(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        @timed
        def preload():
            LSFR.lsfr_from_cache(0)
        # pre-loads the LSFR cache before testing any timed methods
        preload()

    def test_next(self):
        # Given: a freshly-seeded LSFR
        lsfr = LSFR()

        # When:  the next 8 frames are checked
        # Then:  the expected 1st byte is found
        for next_expected in [68, 34, 145, 72, 36, 18, 137, 68]:
            next_actual = lsfr.next()[0]
            self.assertEqual(next_actual, next_expected)

    def test_next_17610(self):
        # Given: the LSFR state for frame 17610
        lsfr = LSFR([0x61, 0x7d, 0xbf, 0x44, 0x3a, 0xb2, 0xc7, 0xa2, 0x2d])

        # When:  the LSFR is incremented to frame 17611
        actual_17611 = lsfr.next()

        # Then:  the expected state is found
        expected_17611 = [0x30, 0xbe, 0xdf, 0xa2, 0x1d, 0x59, 0x63, 0xd1, 0x16]
        self.assertEqual(expected_17611, actual_17611)

    def test_next_n_spot_checks(self):
        # Given: some a pre-known expected LSFR state
        expected_state = [0x61, 0x7d, 0xbf, 0x44, 0x3a, 0xb2, 0xc7, 0xa2, 0x2d]
        # And:   the expected iteration that finds this state (lag frames?)
        expected_iteration = 17598
        # And:   a freshly-seeded LSFR
        lsfr = LSFR()

        # When:  the LSFR is incremented
        actual_iterations = 0
        while lsfr.data != expected_state:
            lsfr.next()
            actual_iterations += 1
            if actual_iterations > 33000:
                self.fail("Didn't work man")

        # Then:  the expected state is achieved at the expected iteration
        self.assertEqual(actual_iterations, expected_iteration)

    def test_lsfr_first_byte_repeating_sequence(self):
        # Given: a fresh LSFR
        lsfr = LSFR()
        # And:   another LSFR that was iterated 2**15 -1 times
        double_lapped_lsfr = LSFR()
        double_lapped_lsfr.next_n(2**15 - 1)

        # When:  the next 10 first bytes are sampled from each LSFR
        fresh_next_10 = [lsfr.next()[1] for _ in range(10)]
        double_lapped_lsfr_next_10 = [double_lapped_lsfr.next()[1] for _ in range(10)]

        # Then:  they will have the same byte sequence
        self.assertEqual(fresh_next_10, double_lapped_lsfr_next_10)

    def test_lsfr_identical_state(self):
        # Given: two freshly-initialized LSFRs
        lsfr_one = LSFR()
        lsfr_two = LSFR()
        # And:   both have iterated enough to clear out the initially blank bytes
        i = 0
        while lsfr_one.random_n(7) & 1 != 1:
            i += 1
            lsfr_one.next()
            lsfr_two.next()
        # And:   it took 67 iterations for a 1 bit to percolate all the way through the LSFR
        self.assertEqual(i, 67)

        # When:  the second LSFR is iterated an additional 2**15 -1 times
        lsfr_two.next_n(2**15 - 1)

        # Then:  the two LSFR states match perfectly
        self.assertEqual(lsfr_one.data, lsfr_two.data)

    @unittest.skip("runs a little slow")
    def test_next_n_optmized_matches(self):
        # Given: a large number of iters
        iters = 500000

        # When:  the iterations are processed (unoptimized)
        unoptimized_lsfr = timed_lsfr_fixture(iters, optimize=False)
        # And:   the same iterations are processed (optimized)
        optimized_lsfr = timed_lsfr_fixture(iters, optimize=True)

        # Then:  the two LSFRs' data matches
        self.assertEqual(unoptimized_lsfr.data, optimized_lsfr.data)

    def test_lsfr_from_cache(self):
        # Given: a large number of iters
        iters = 500000
        # And:   a manually computed LSFR
        manual_lsfr = timed_lsfr_fixture(iters)

        # When:  the LSFR for this iteration is fetched from cache
        cached_lsfr = timed_lsfr_from_cache(iters)

        # Then:  it matches
        self.assertEqual(manual_lsfr.data, cached_lsfr.data)

    def test_for_iteration_n(self):
        # Given: a few different target iterations
        iterations_to_check = [10, 500, 5000, 50000, 500000, 5000000]

        # When:  the for_iteration_n() class method is used
        # Then:  the resulting LSFR's state exactly matches the manually iterated LSFR's state
        for iteration in iterations_to_check:
            with self.subTest(iteration=iteration):
                manual_lsfr = LSFR()
                manual_lsfr.next_n(iteration)
                lsfr_for_n = LSFR.for_iteration_n(iteration)
                self.assertEqual(manual_lsfr.data, lsfr_for_n.data)

    def test_lsfr_from_cache_iteration_n(self):
        # Given: a few different target iterations
        iterations_to_check = [10, 500, 5000, 50000, 500000, 5000000]

        # When:  the for_iteration_n() class method is used
        # Then:  the resulting LSFR's state exactly matches the manually iterated LSFR's state
        for iteration in iterations_to_check:
            with self.subTest(iteration=iteration):
                manual_lsfr = LSFR()
                manual_lsfr.next_n(iteration)
                from_cache_n = LSFR.lsfr_from_cache(iteration)
                self.assertEqual(manual_lsfr.data, from_cache_n.data)

    def test_iter_from_cache_byte_list(self):
        actual_iteration = timed_iter_from_cache([156, 167, 158, 209, 236, 79, 151, 8, 38])
        self.assertEqual(actual_iteration, 25604)

    def test_iter_from_cache_str(self):
        actual_iteration = timed_iter_from_cache('9c a7 9e d1 ec 4f 97 08 26')
        self.assertEqual(actual_iteration, 25604)

    def test_clone(self):
        lsfr = LSFR()
        lsfr.next_n(5)
        lsfr_clone = lsfr.clone()
        lsfr_clone.next()
        self.assertNotEqual(lsfr.get(0), lsfr_clone.get(0))

    def test_hand_check(self):
        lsfr = LSFR([156, 167, 158, 209, 236, 79, 151, 8, 38])
        self.assertFalse(lsfr.hand_check())
        lsfr = LSFR([201, 142, 29, 1, 59, 57, 79, 61, 163])
        self.assertTrue(lsfr.hand_check())

        lsfr = LSFR([103, 41, 231, 180, 123, 19, 229, 194, 9])
        self.assertFalse(lsfr.hand_check())
        lsfr = LSFR([242, 99, 135, 64, 78, 206, 83, 207, 104])
        self.assertFalse(lsfr.hand_check())
        lsfr = LSFR([221, 72, 242, 99, 135, 64, 78, 206, 83])
        self.assertTrue(lsfr.hand_check())

    def test_from_hex_str(self):
        actual_hex_arr = from_hex_str("9c a7 9e d1 ec 4f 97 08 26")
        self.assertEqual(actual_hex_arr, [156, 167, 158, 209, 236, 79, 151, 8, 38])


@timed
def timed_lsfr_fixture(iters: int, optimize: bool = True) -> LSFR:
    lsfr = LSFR()
    lsfr.next_n(iters, optimize=optimize)
    return lsfr

@timed
def timed_lsfr_from_cache(iters: int) -> LSFR:
    return LSFR.lsfr_from_cache(iters)

@timed
def timed_iter_from_cache(data) -> int:
    return LSFR.iter_from_cache(data)
