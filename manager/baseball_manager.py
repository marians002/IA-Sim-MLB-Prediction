def get_state_representation(game_state):
    # Convert game state to a tuple or string representation
    return game_state.inning, game_state.outs, game_state.score_difference


# class BaseballManager:
#     def __init__(self, rules):
#         self.rules = rules
#         # self.learning_agent = learning_agent
#
#     def add_rule(self, rule):
#         self.rules.append(rule)
#
#     def evaluate_rules(self, game_state):
#         # state = get_state_representation(game_state)
#         # action_name = self.learning_agent.choose_action(state)
#         # action = next((rule.action for rule in self.rules if rule.action.__name__ == action_name), None)
#         # if action:
#             # return action
#         for rule in self.rules:
#             if rule.condition(game_state):
#                 return rule.name
#         return "No action"


class BaseballManager:
    def __init__(self, beliefs, desires, intentions):
        self.beliefs = beliefs
        self.desires = desires
        self.intentions = intentions

    def perceive(self, game_state):
        for belief in self.beliefs:
            if belief.evaluate(game_state):
                print(f"Belief {belief.name} is true")

    def generate_desires(self, game_state):
        active_desires = []
        for desire in self.desires:
            if desire.evaluate(game_state):
                active_desires.append(desire)
                print(f"Desire {desire.name} is active")
        return active_desires

    def filter_intentions(self, active_desires):
        active_intentions = []
        for desire in active_desires:
            for intention in self.intentions:
                if intention.name == desire.name:
                    active_intentions.append(intention)
                    print(f"Intention {intention.name} is selected")
        return active_intentions

    def execute_intentions(self, game_state, active_intentions):
        for intention in active_intentions:
            result = intention.execute(game_state)
            print(f"Executed intention {intention.name}: {result}")

    def run(self, game_state):
        self.perceive(game_state)
        active_desires = self.generate_desires(game_state)
        active_intentions = self.filter_intentions(active_desires)
        self.execute_intentions(game_state, active_intentions)
