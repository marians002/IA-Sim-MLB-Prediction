class Belief:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

    def evaluate(self, game_state):
        return self.condition(game_state)


class Desire:
    def __init__(self, name, goal):
        self.name = name
        self.goal = goal

    def evaluate(self, game_state):
        return self.goal(game_state)


class Intention:
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def execute(self, game_state):
        return self.action(game_state)
