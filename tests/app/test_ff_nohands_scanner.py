import unittest

from smb3_eh_manip.app.ff_nohands_scanner import NoHandsScanner, get_pascal_row


class TestFFNoHandsScanner(unittest.TestCase):

    scanner: NoHandsScanner = None

    @classmethod
    def setUpClass(cls):
        cls.scanner = NoHandsScanner(minutes_to_scan=60,
                                     score_cap=14)

    def test_show_good_hand_sequences(self):
        TestFFNoHandsScanner.scanner.show_good_hand_sequences()

    def test_scan_for_ideal_good_hand_sequences(self):
        # fiddle with statistics:
        # min score mean (avg):  ignores all no-hands sequences below this average set score
        # max score std dev:     ignores all no-hands sequences above the given variance (diff between weighted scores)
        ideal_matches = TestFFNoHandsScanner.scanner.scan_for_ideal_good_hand_sequences(min_score_mean = 8.0,
                                                                                        max_score_std_dev = 8.0,
                                                                                        only_streaks=True,
                                                                                        iter_range=(150000, 165000))
        for match in ideal_matches:
            print(match)

    def test_get_pascal_row_no_cap(self):
        inputs_expected_output = [
            (1, [1]),
            (2, [1, 1]),
            (3, [1, 2, 1]),
            (4, [1, 3, 3, 1])
        ]
        for (row, expected_output) in inputs_expected_output:
            with self.subTest(row=row):
                actual_output = get_pascal_row(row)
                self.assertEqual(expected_output, actual_output)

    def test_get_pascal_row_capped_score(self):
        # Given: a good hand streak
        streak = 8
        # And:   a score capped at 12
        score_cap = 12

        # When:  that streak is scored
        actual_scores = get_pascal_row(streak, score_cap=score_cap)

        # Then:  no score exceeds the score cap
        self.assertEqual(actual_scores, [1, 7, 12, 12, 12, 12, 7, 1])
