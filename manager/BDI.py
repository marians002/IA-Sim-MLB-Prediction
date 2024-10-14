from manager.intentions import *
from manager.beliefs import *


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


def define_bdi():
    b_change_pitcher = Belief("Change Pitcher", change_pitcher_condition)
    b_steal_base = Belief("Steal Base", steal_base_condition)
    b_bunt = Belief("Bunt", bunt_condition)
    b_pinch_hitter = Belief("Pinch Hitter", pinch_hitter_condition)
    b_hit_and_run = Belief("Hit and Run", hit_and_run_condition)
    b_intentional_walk = Belief("Intentional Walk", intentional_walk_condition)
    b_pickoff = Belief("Pickoff", pickoff_condition)
    b_infield_in = Belief("Infield In", infield_in_condition)

    b = [b_change_pitcher, b_steal_base, b_bunt, b_pinch_hitter, b_hit_and_run,
         b_intentional_walk, b_pickoff, b_infield_in]
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
        Desire("Pickoff", b_pickoff),
        Desire("Infield In", b_infield_in)
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
        Intention("Infield In", infield_in_action)
    ]
    return b, d, i


class BDI:
    def __init__(self):
        self.beliefs, self.desires, self.intentions = define_bdi()

    def add_belief(self, name, condition):
        self.beliefs.append(Belief(name, condition))

    def add_desire(self, name, type, goal):
        self.desires[type].append(Desire(name, goal))

    def add_intention(self, name, action):
        self.intentions.append(Intention(name, action))

    def remove_belief(self, name):
        for belief in self.beliefs:
            if belief.name == name:
                self.beliefs.remove(belief)
                break

    def remove_desire(self, name, type):
        for desire in self.desires[type]:
            if desire.name == name:
                self.desires[type].remove(desire)
                break

    def remove_intention(self, name):
        for intention in self.intentions:
            if intention.name == name:
                self.intentions.remove(intention)
                break
