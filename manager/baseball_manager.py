def get_state_representation(game_state):
    # Convert game state to a tuple or string representation
    return game_state.inning, game_state.outs, game_state.score_difference


class BaseballManager:
    def __init__(self, rules, learning_agent):
        self.rules = rules
        self.learning_agent = learning_agent

    def add_rule(self, rule):
        self.rules.append(rule)

    def evaluate_rules(self, game_state):
        state = get_state_representation(game_state)
        action_name = self.learning_agent.choose_action(state)
        action = next((rule.action for rule in self.rules if rule.action.__name__ == action_name), None)
        if action:
            return action
        return "No action"

