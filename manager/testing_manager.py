from BDI import *
from manager.rules_action import *
from manager.rules_conditions import *


def determine_manager_type(game_state):
    if game_state.inning >= 7 and game_state.score_difference <= 2:
        return "conservative"
    elif game_state.inning < 7 and game_state.score_difference < 0:
        return "aggressive"
    elif game_state.inning >= 7 and game_state.score_difference > 2:
        return "defensive"
    return "neutral"


def execute_intentions(game_state, active_intentions):
    for intention in active_intentions:
        result = intention.execute(game_state)
        print(f"Executed intention {intention.name}: {result}")


class BaseballManager:
    def __init__(self, beliefs, desires, intentions):
        self.beliefs = beliefs
        self.desires = desires
        self.intentions = intentions

    def generate_desire(self, game_state, manager_type):
        for desire in self.desires[manager_type]:
            if desire.evaluate(game_state):
                # print(f"Desire {desire.name} is active")
                return desire.name
        return "No action"

    def filter_intentions(self, active_desire):
        for intention in self.intentions:
            if intention.name == active_desire.name:
                print(f"Intention {intention.name} is selected")
                return intention
        return None

    def run(self, game_state):
        manager_type = determine_manager_type(game_state)
        active_desire = self.generate_desire(game_state, manager_type)
        if active_desire:
            active_intention = self.filter_intentions(active_desire)
            if active_intention:
                execute_intentions(game_state, [active_intention])


# Define goals for different types of managers
def conservative_manager(game_state):
    return game_state.inning >= 7 and game_state.score_difference <= 2


def aggressive_manager(game_state):
    return game_state.inning < 7 and game_state.score_difference < 0


def defensive_manager(game_state):
    return game_state.inning >= 7 and game_state.score_difference > 2


beliefs = [
    Belief("Change Pitcher", change_pitcher_condition),
    Belief("Steal Base", steal_base_condition),
    Belief("Bunt", bunt_condition),
    Belief("Pinch Hitter", pinch_hitter_condition),
    Belief("Hit and Run", hit_and_run_condition),
    Belief("Intentional Walk", intentional_walk_condition),
    Belief("Pickoff", pickoff_condition)
]

# Create desire instances for different types of managers
desires = {
    "conservative": [
        Desire("Change Pitcher", conservative_manager),
        Desire("Intentional Walk", conservative_manager)
    ],
    "aggressive": [
        Desire("Steal Base", aggressive_manager),
        Desire("Hit and Run", aggressive_manager)
    ],
    "defensive": [
        Desire("Bunt", defensive_manager),
        Desire("Pickoff", defensive_manager)
    ],
    "neutral": []  # Add neutral desires if needed
}

intentions = [
    Intention("Change Pitcher", change_pitcher_action),
    Intention("Steal Base", steal_base_action),
    Intention("Bunt", bunt_action),
    Intention("Pinch Hitter", pinch_hitter_action),
    Intention("Hit and Run", hit_and_run_action),
    Intention("Intentional Walk", intentional_walk_action),
    Intention("Pickoff", pickoff_action)
]

# Create instances of BaseballManager with beliefs, desires, and intentions
manager = BaseballManager(beliefs, desires, intentions)
