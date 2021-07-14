from abc import ABC, abstractmethod
from collections import Counter
from typing import List, Optional


class RuleNotMetError(Exception):
    """Applies to cases where the rule requirements are not met."""


class Rule(ABC):
    """ABC to be implemented for every rule definition."""
    final_score: Optional[int] = None

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        """The user-friendly name of the rule."""
        return self._name

    @abstractmethod
    def calculate_value(self, dice_values: List[int]) -> int:
        """Used to calculate the value based on die values"""
        pass


class UpperSectionRule(Rule):
    def __init__(self, name: str, die_value: int):
        """Special init so this rule's value can be calc'd dynamically."""
        super(UpperSectionRule, self).__init__(name)
        self._die_value = die_value

    def calculate_value(self, dice_values: List[int]) -> int:
        """All Upper Section Rules are just the sum of the rule's die value."""
        val_count = len([d for d in dice_values if d == self._die_value])

        if not val_count:
            raise RuleNotMetError(f'There must be at least one die on '
                                  f'{self._die_value} in order to score on {self.name}')
        else:
            return val_count * self._die_value


class Aces(UpperSectionRule):
    def __init__(self):
        super(Aces, self).__init__('Aces', 1)


class Twos(UpperSectionRule):
    def __init__(self):
        super(Twos, self).__init__('Twos', 2)


class Threes(UpperSectionRule):
    def __init__(self):
        super(Threes, self).__init__('Threes', 3)


class Fours(UpperSectionRule):
    def __init__(self):
        super(Fours, self).__init__('Fours', 4)


class Fives(UpperSectionRule):
    def __init__(self):
        super(Fives, self).__init__('Fives', 5)


class Sixes(UpperSectionRule):
    def __init__(self):
        super(Sixes, self).__init__('Sixes', 6)


class XOfAKindRule(Rule):
    """Base class for X of a Kind rules."""

    def __init__(self, name, count_needed: int):
        """Special initialization so these can be calc'd dynamically."""
        super(XOfAKindRule, self).__init__(name)
        self.count_needed = count_needed

    def calculate_value(self, dice_values: List[int]) -> int:
        if not self.validate(dice_values):
            raise RuleNotMetError(f'{self.count_needed} of a kind requires '
                                  f'{self.count_needed} or more of any value.')

        return sum(dice_values)

    def validate(self, dice_values: List[int]) -> bool:
        """Validation fn defined separately just to keep things tidy here."""
        counts = Counter(dice_values).values()
        if not any([c >= self.count_needed for c in counts]):
            return False
        return True


class ThreeOfAKind(XOfAKindRule):
    def __init__(self):
        super(ThreeOfAKind, self).__init__('3 of a Kind', 3)


class FourOfAKind(XOfAKindRule):
    def __init__(self):
        super(FourOfAKind, self).__init__('4 of a Kind', 4)


class FullHouse(Rule):
    def __init__(self):
        super(FullHouse, self).__init__('Full House')

    def calculate_value(self, dice_values: List[int]) -> int:
        counts = Counter(dice_values).values()
        if 3 in counts and 2 in counts:
            return 25

        raise RuleNotMetError('You must have 3 of one value and 2 of another for a Full House.')


class SmallStraight(Rule):
    def __init__(self):
        super(SmallStraight, self).__init__('Small Straight')

    def calculate_value(self, dice_values: List[int]) -> int:
        if not any({i + 1, i + 2, i + 3} < set(dice_values) for i in dice_values):
            raise RuleNotMetError('You must have at least 4 consecutive dice values for a small straight.')

        return 30


class LargeStraight(Rule):
    def __init__(self):
        super(LargeStraight, self).__init__('Large Straight')

    def calculate_value(self, dice_values: List[int]) -> int:
        if not any({i + 1, i + 2, i + 3, i + 4} < set(dice_values) for i in dice_values):
            raise RuleNotMetError('You must have at least 5 consecutive dice values for a small straight.')

        return 40


class Yahtzee(XOfAKindRule):
    def __init__(self):
        super(Yahtzee, self).__init__('Yahtzee (5 of a Kind)', 5)

    def calculate_value(self, dice_values: List[int]) -> int:
        """
        Overridden since this is calc'd differently, but the same validation still applies.
        """
        if not self.validate(dice_values):
            raise RuleNotMetError('You must have at least 5 of a kind in order to Yahtzee')
        return 50


class Chance(Rule):
    def __init__(self):
        super(Chance, self).__init__('Chance')

    def calculate_value(self, dice_values: List[int]) -> int:
        return sum(dice_values)
