import unittest

from yahtzee import rules


class TestUpperSectionRules(unittest.TestCase):
    def test_aces(self):
        """
        Test of Aces Rule
        """
        passing_vals = [1, 2, 3, 4, 1]
        failing_vals = [2, 2, 3, 4, 2]
        rule = rules.Aces()
        self.assertEqual(2, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_twos(self):
        """
        Test of Twos Rule
        """
        passing_vals = [1, 2, 2, 4, 1]
        failing_vals = [1, 1, 3, 4, 1]
        rule = rules.Twos()
        self.assertEqual(4, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_threes(self):
        """
        Test of Threes Rule
        """
        passing_vals = [1, 2, 3, 4, 1]
        failing_vals = [2, 2, 2, 4, 2]
        rule = rules.Threes()
        self.assertEqual(3, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_fours(self):
        """
        Test of Fours Rule
        """
        passing_vals = [4, 4, 2, 3, 2]
        failing_vals = [1, 2, 3, 2, 2]
        rule = rules.Fours()

        self.assertEqual(8, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_fives(self):
        """
        Test of Fives Rule
        """
        passing_vals = [5, 5, 5, 3, 2]
        failing_vals = [1, 2, 3, 2, 2]
        rule = rules.Fives()

        self.assertEqual(15, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_sixes(self):
        """
        Test of Sixes Rule
        """
        passing_vals = [6, 6, 2, 3, 2]
        failing_vals = [1, 2, 3, 2, 2]
        rule = rules.Sixes()

        self.assertEqual(12, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)


class TestXOfAKindRules(unittest.TestCase):
    def test_three_of_a_kind(self):
        """
        Test Three of a Kind Rule
        """
        passing_vals = [1, 1, 1, 2, 3]
        failing_vals = [1, 2, 3, 4, 5]
        rule = rules.ThreeOfAKind()

        self.assertEqual(8, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_four_of_a_kind(self):
        """
        Test Four of a Kind Rule
        """
        passing_vals = [1, 1, 1, 1, 3]
        failing_vals = [1, 2, 3, 4, 5]
        rule = rules.FourOfAKind()

        self.assertEqual(7, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_yahtzee(self):
        """
        Test Yahtzee (5 of a Kind) Rule
        """
        passing_vals = [1, 1, 1, 1, 1]
        failing_vals = [1, 2, 3, 4, 5]
        rule = rules.Yahtzee()

        self.assertEqual(50, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)


class TestOtherRules(unittest.TestCase):
    def test_full_house(self):
        """
        Test Full House Rule
        """
        passing_vals = [1, 1, 1, 2, 2]
        failing_vals = [1, 2, 3, 4, 5]
        rule = rules.FullHouse()

        self.assertEqual(25, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_small_straight(self):
        """
        Test Small Straight Rule
        """
        passing_vals = [1, 2, 3, 4, 6]
        failing_vals = [1, 1, 1, 2, 2]
        rule = rules.SmallStraight()

        self.assertEqual(30, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_large_straight(self):
        """
        Test Large Straight
        """
        passing_vals = [1, 2, 3, 4, 5]
        failing_vals = [1, 1, 1, 2, 2]
        rule = rules.LargeStraight()

        self.assertEqual(40, rule.calculate_value(passing_vals))
        self.assertRaises(rules.RuleNotMetError, rule.calculate_value, failing_vals)

    def test_chance(self):
        passing_vals = [1, 2, 3, 4, 5]
        rule = rules.Chance()

        self.assertEqual(15, rule.calculate_value(passing_vals))


if __name__ == '__main__':
    unittest.main(verbosity=2)
