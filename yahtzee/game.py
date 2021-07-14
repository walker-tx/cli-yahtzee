from random import randint
from typing import List

from yahtzee.die import Die
from yahtzee.rules import Rule, RuleNotMetError


class IncompleteTurnError(Exception):
    """Exception for when the turn hasn't been completed."""


class DieController:
    """Controls the behavior of the die passed to it."""
    die: Die
    holding: bool = False

    def __init__(self, die: Die):
        self.die = die

    @property
    def value(self) -> int:
        """Value that the die is currently on."""
        return self.die.value

    def roll(self) -> None:
        """Rolls the die only if it's not being held."""
        if not self.holding:
            self.die.value = randint(1, 6)


class RuleController:
    """
    Tracks the status of each rule and provides some logic to help facilitate the game.

    NOTE: I'm not sure that I like the fact that this class knows about the dice.
    """
    _rule: Rule
    _locked_in: bool = False
    _locked_value: int = 0
    _dice_ref: List[Die]

    def __init__(self, rule: Rule, dice_ref: List[Die]):
        self._rule = rule
        self._dice_ref = dice_ref

    @property
    def rule_name(self):
        """Just a pass-through for the rule's friendly name."""
        return self._rule.name

    @property
    def locked_in(self):
        """Represents whether the rule has been locked-in or not."""
        return self._locked_in

    @property
    def locked_value(self):
        """The value that the object was locked-in with."""
        return self._locked_value

    def calculate_value(self):
        """Calculates the value of the rule with the given dice and return 0 if the rule is not met."""
        die_values = [d.value for d in self._dice_ref]
        try:
            return self._rule.calculate_value(dice_values=die_values)
        except RuleNotMetError:
            return 0

    def lock_in(self):
        """Locks in the rule's current value and changes the controller's status."""
        if not self.locked_in:
            self._locked_in = True
            self._locked_value = self.calculate_value()


class Game:
    """
    Class to control the dice, rules, and scoring.
    """
    dice: List[Die]
    die_controllers: List[DieController]
    rule_controllers: List[RuleController] = []
    roll_count = 0

    def __init__(self):
        self.dice = [Die() for _ in range(5)]
        self.die_controllers = [DieController(d) for d in self.dice]

    def register_rule(self, rule: Rule):
        self.rule_controllers.append(RuleController(rule, self.dice))

    def lock_in_rule(self, rule_controller: RuleController):
        rule_controller.lock_in()

        for dc in self.die_controllers:
            dc.holding = False

        self.roll_count = 0
        self.roll()

    @property
    def score(self):
        return sum([r.locked_value for r in self.rule_controllers])

    def roll(self):
        if self.roll_count >= 3:
            raise IncompleteTurnError("You must lock in a rule before rolling again.")

        for slot in self.die_controllers:
            slot.roll()

        self.roll_count += 1

    @property
    def game_over(self):
        return all([rc.locked_in for rc in self.rule_controllers])

    @property
    def locked_rules_count(self):
        return len([rc for rc in self.rule_controllers if rc.locked_in])
