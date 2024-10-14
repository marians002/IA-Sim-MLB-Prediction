from manager.BDI import Belief, Desire, Intention
from manager.intentions import *
from manager.beliefs import *
from manager.desires import *
import random


def define_bdi():
    b_change_pitcher = Belief("Change Pitcher", change_pitcher_condition)
    b_steal_base = Belief("Steal Base", steal_base_condition)
    b_bunt = Belief("Bunt", bunt_condition)
    b_pinch_hitter = Belief("Pinch Hitter", pinch_hitter_condition)
    b_hit_and_run = Belief("Hit and Run", hit_and_run_condition)
    b_intentional_walk = Belief("Intentional Walk", intentional_walk_condition)
    b_pickoff = Belief("Pickoff", pickoff_condition)

    b = [b_change_pitcher, b_steal_base, b_bunt, b_pinch_hitter, b_hit_and_run, b_intentional_walk, b_pickoff]
    # Create desire instances for different types of managers

    conservative_desires = [
        Desire("Change Pitcher", b_change_pitcher),
        Desire("Intentional Walk", b_intentional_walk)
    ]
    aggressive_desires = [
        Desire("Steal Base", b_steal_base),
        Desire("Hit and Run", b_hit_and_run),
        Desire("Pinch Hitter", b_pinch_hitter)
    ]
    defensive_desires = [
        Desire("Bunt", b_bunt),
        Desire("Pickoff", b_pickoff)
    ]
    neutral_desires = conservative_desires + aggressive_desires + defensive_desires

    d = {
        "conservative": conservative_desires,
        "aggressive": aggressive_desires,
        "defensive": defensive_desires,
        "neutral": neutral_desires
    }

    i = [
        Intention("Change Pitcher", change_pitcher_action),
        Intention("Steal Base", steal_base_action),
        Intention("Bunt", bunt_action),
        Intention("Pinch Hitter", pinch_hitter_action),
        Intention("Hit and Run", hit_and_run_action),
        Intention("Intentional Walk", intentional_walk_action),
        Intention("Pickoff", pickoff_action),
    ]
    return b, d, i


class BaseballManager:
    def __init__(self):
        self.team_batting = False
        self.beliefs, self.desires, self.intentions = define_bdi()

    def set_batting(self, flag: bool):
        self.team_batting = flag

    def generate_desire(self, game_state, selected_rules):
        for desire in selected_rules:
            if desire.goal.evaluate(game_state):
                return desire.name
        return "No action"

    def filter_intentions(self, active_desire):
        for intention in self.intentions:
            if intention.name == active_desire:
                return intention
        return Intention("No action", lambda x: (None, 'No action taken'))

    def get_manager_rules(self, game_state):
        percentages = evaluate_manager_types(game_state)
        types = ["conservative", "aggressive", "defensive", "neutral"]
        num_rules = 2  # Total number of rules to select
        selected_rules = []

        for i, manager_type in enumerate(types):
            num_type_rules = round((percentages[manager_type] / 100) * num_rules)
            selected_rules.extend(random.sample(self.desires[manager_type], num_type_rules))

        return selected_rules

    def run(self, game_state):
        selected_rules = self.get_manager_rules(game_state)
        active_desire = self.generate_desire(game_state, selected_rules)
        return self.filter_intentions(active_desire)

