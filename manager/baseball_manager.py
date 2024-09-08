class BaseballManager:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def evaluate_rules(self, game_state):
        for rule in self.rules:
            if rule(game_state):
                return rule.__name__
        return "No action"
