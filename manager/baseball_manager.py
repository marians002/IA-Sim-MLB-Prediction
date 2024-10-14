from manager.BDI import *
from manager.desires import *
import random


class BaseballManager:
    def __init__(self):
        self.team_batting = False
        self.BDI = BDI()

    def set_batting(self, flag: bool):
        self.team_batting = flag

    def generate_desire(self, game_state, selected_rules):
        for desire in selected_rules:
            if desire.goal.evaluate(game_state):
                return desire.name
        return "No action"

    def filter_intentions(self, active_desire):
        for intention in self.BDI.intentions:
            if intention.name == active_desire:
                return intention
        return Intention("No action", lambda x: (None, 'No action taken'))

    def get_manager_rules(self, game_state):
        percentages = evaluate_manager_types(game_state)
        types = percentages.keys()
        num_rules = 2  # Total number of rules to select
        selected_rules = []

        for i, manager_type in enumerate(types):
            num_type_rules = round((percentages[manager_type] / 100) * num_rules)
            selected_rules.extend(random.sample(self.BDI.desires[manager_type], num_type_rules))

        return selected_rules

    def run(self, game_state):
        selected_rules = self.get_manager_rules(game_state)
        active_desire = self.generate_desire(game_state, selected_rules)
        return self.filter_intentions(active_desire)
