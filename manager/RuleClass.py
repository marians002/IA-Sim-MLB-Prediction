class Rule:
    def __init__(self, name, condition, action):
        self.name = name
        self.condition = condition
        self.action = action

    def evaluate(self, game_state):
        if self.condition(game_state):
            return self.action
        return None


