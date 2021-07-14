import sys
from dataclasses import dataclass
from typing import Dict, Callable, Optional

import tabulate
from inquirer2 import prompt, Separator

from yahtzee.game import Game, IncompleteTurnError
from yahtzee.rules import (Aces, Twos, Threes, Fours, Fives, Sixes, ThreeOfAKind, FourOfAKind, FullHouse, SmallStraight,
                           LargeStraight, Yahtzee, Chance)

rules = [
    Aces(),
    Twos(),
    Threes(),
    Fours(),
    Fives(),
    Sixes(),
    ThreeOfAKind(),
    FourOfAKind(),
    FullHouse(),
    SmallStraight(),
    LargeStraight(),
    Yahtzee(),
    Chance()
]


@dataclass
class State:
    next: str
    context: dict


class StateMachine:
    """
    State Machine to display views (prompts), and allow the user to
    interact with the Game object
    """
    current_state: State = State("PROMPTING_MAIN_MENU", {})
    game: Game
    state_map: Dict[str, Callable[[], Optional[State]]]

    def __init__(self, game: Game):
        self.game = game
        self.state_map = {
            "PROMPTING_MAIN_MENU": self.prompting_main_menu,
            "PROMPTING_INSTRUCTIONS": self.prompting_instructions,
            "STARTING_GAME": self.starting_game,
            "PROMPTING_GAME_MAIN": self.prompting_game_main,
            "PROMPTING_HOLD": self.prompting_hold,
            "ROLLING": self.rolling,
            "PROMPTING_RULES": self.prompting_rules,
            "TERMINATING": self.terminating
        }

    def starting_game(self) -> State:
        """Initial setup for the game."""
        self.game.roll()
        return State("PROMPTING_GAME_MAIN", {})

    def prompting_main_menu(self) -> State:
        print("__   __    _     _                ")
        print("\\ \\ / /   | |   | |               ")
        print(" \\ V /__ _| |__ | |_ _______  ___ ")
        print("  \\ // _\\` | '_ \\| __|_  / _ \\/ _ \\")
        print("  | | (_| | | | | |_ / /  __/  __/")
        print("  \\_/\\__,_|_| |_|\\__/___\\___|\\___|")
        print("---")

        answer = prompt.prompt([{
            "type": "list",
            "name": "next",
            "message": "What would you like to do?",
            "choices": [
                {"name": "Play a game", "value": State("STARTING_GAME", {})},
                {"name": "Read the instructions", "value": State("PROMPTING_INSTRUCTIONS", {})}
            ]
        }]).get("next", State("STARTING_GAME", {}))

        return answer

    def display_dice(self):
        die_tbl_rows = [['In-Play'], ['Holding']]
        for dc in self.game.die_controllers:
            if not dc.holding:
                die_tbl_rows[0].append(str(dc.value))
                die_tbl_rows[1].append(' ')
            else:
                die_tbl_rows[0].append(' ')
                die_tbl_rows[1].append(str(dc.value))

        print("---")
        print("Dice:")
        print(tabulate.tabulate(die_tbl_rows, tablefmt="fancy_grid"))
        print("Turn:", self.game.locked_rules_count + 1,
              "Roll: ", self.game.roll_count,
              "Score: ", self.game.score)
        print("---")

    def prompting_instructions(self) -> State:
        print("INSTRUCTIONS:")
        print("On each turn, roll the dice up to 3 times to get the highest\n"
              "scoring combinations for one of 13 Scoring Categories. After you\n"
              "finish rolling, you must lock-in your score on a category, which\n"
              "is zero if the category isn't met. The game ends when all \n"
              "Scoring Categories have been locked in. The final score is the\n"
              "sum of the locked-in values, including any bonus points.")
        print("---")
        input("Press ENTER to return...")
        return State("PROMPTING_MAIN_MENU", {})

    def prompting_game_main(self) -> State:
        self.display_dice()

        return prompt.prompt([{
            "type": "list",
            "name": "next",
            "message": "What would you like to do?",
            "choices": [
                {"name": "Hold or Release Dice", "value": State("PROMPTING_HOLD", {})},
                {"name": "Roll", "value": State("ROLLING", {})},
                {"name": "View Scoring Categories", "value": State("PROMPTING_RULES", {})}
            ]
        }]).get("next", State("TERMINATING", {"message": "Please select a valid option."}))

    def prompting_hold(self) -> State:
        choices = []
        for dc in self.game.die_controllers:
            choices.append({"name": str(dc.value), "checked": dc.holding, "value": dc})

        answers = prompt.prompt([{
            "type": "checkbox",
            "name": "selections",
            "message": "Select/De-Select the dice you would like to hold/un-hold:",
            "choices": choices
        }])

        for dc in self.game.die_controllers:
            if dc in answers["selections"]:
                dc.holding = True
            else:
                dc.holding = False

        return State("PROMPTING_GAME_MAIN", {})

    def rolling(self) -> State:
        try:
            self.game.roll()
        except IncompleteTurnError:
            print("Lock in a rule before continuing to the next turn")
            return State("PROMPTING_RULES", {"selection_required": True})

        return State("PROMPTING_GAME_MAIN", {})

    def prompting_rules(self) -> State:
        self.display_dice()

        choices = []
        for rc in self.game.rule_controllers:
            choices.append({
                "name": f"{rc.rule_name} [{(rc.locked_value or rc.calculate_value())}]",
                "disabled": "LOCKED" if rc.locked_in else None,
                "value": rc
            })

        if not self.current_state.context.get("selection_required", False):
            choices.extend([Separator(), {"name": "Go Back", "value": "BACK"}])

        answer = prompt.prompt([{
            "type": "list",
            "name": "selection",
            "message": "Select the rule you'd like to lock in:",
            "choices": choices
        }])

        if answer["selection"] != "BACK":
            self.game.lock_in_rule(answer["selection"])

        return State("PROMPTING_GAME_MAIN", {})

    def terminating(self) -> None:
        if msg := self.current_state.context.get("message"):
            print(msg)
        sys.exit(0)

    def run(self, verbose=False):
        while not self.game.game_over:
            next_state = self.current_state.next
            if verbose:
                print(next_state)

            try:
                self.current_state = self.state_map[next_state]()
            except KeyError:
                self.current_state = State("TERMINATING",
                                           {"message": f"Not yet implemented: {next_state}"})

        print("Game Over!")
        print("Score:", self.game.score)


def main():
    game = Game()

    for rule in rules:
        game.register_rule(rule)

    game_runner = StateMachine(game)
    game_runner.run()


if __name__ == '__main__':
    main()
