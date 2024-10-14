class Belief:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

    def evaluate(self, game_state):
        return self.condition(game_state)


class Desire:
    def __init__(self, name, goal: Belief):
        self.name = name
        self.goal = goal


class Intention:
    def __init__(self, name, action):
        self.name = name
        self.action = action
