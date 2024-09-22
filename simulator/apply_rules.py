import random
from simulator.game_state import *


def speed_rate(batter):
    return batter.sprint_speed / 35  # Assuming 35 mph as an upper limit


def change_pitcher(game_state: GameState, bullpen):
    if len(bullpen) > 1:
        new_pitcher = bullpen.pop(random.randint(1, len(bullpen) - 1))
        game_state.update(pitch_count=0, pitcher=new_pitcher)
        return new_pitcher, f"New pitcher is now {new_pitcher.first_name} {new_pitcher.last_name}"
    return None, 'No more pitchers available.'


# Modify the batter for the runner on 1st base
def steal_base_rule(game_state: GameState):
    steal_probability = speed_rate(game_state.batter)
    if random.random() < steal_probability:
        game_state.advance_runners(bases=1)
        game_state.remove_runners(1)
        return f"{game_state.batter.first_name} {game_state.batter.last_name} successfully stole the base!"
    else:
        game_state.remove_runners(bases=1)
        game_state.update(outs=game_state.outs + 1)
        return f"{game_state.batter.first_name} {game_state.batter.last_name} was caught stealing."


def bunt_rule(game_state: GameState):
    # Convert sprint_speed from mph to a percentage (assuming 35 mph as an upper limit)
    speed = speed_rate(game_state.batter)
    # Calculate probabilities
    bunt_success_probability = (speed + game_state.batter.avg) / 2
    bunt_effective_probability = bunt_success_probability / 2

    random_value = random.random()
    # The batter was out. No one advances
    if random_value < bunt_effective_probability:
        return 'out', f"{game_state.batter.first_name} {game_state.batter.last_name} was out on the bunt attempt."
    # Everyone advances one base, batter is out
    elif random_value < bunt_success_probability:
        return 'bunt', (f"{game_state.batter.first_name} {game_state.batter.last_name} bunted effectively: "
                        f"He is out but runners advance!")
    else:

        return 'single', (f"{game_state.batter.first_name} {game_state.batter.last_name} successfully bunted, batter "
                          f"and runners advance!")


def pinch_hitter_rule(game_state: GameState, batters, lineup, current_batter):
    # Get the batter with the highest average if it is not in the current lineup
    new_batter = max(batters, key=lambda x: x.avg if x not in lineup else 0)
    if new_batter.avg > game_state.batter.avg:
        # Modify the lineup
        lineup[current_batter] = new_batter
        return f"Pinch hitter {new_batter.first_name} {new_batter.last_name} is coming in!"


def hit_and_run_rule(game_state: GameState):
    speed = speed_rate(game_state.batter)
    hit_run_prob = (game_state.batter.avg + speed) / 2
    if random.random() < hit_run_prob:
        return 'hitrun', f"{game_state.batter.first_name} {game_state.batter.last_name} successfully executed a hit and run!"
    return 'out', f"{game_state.batter.first_name} {game_state.batter.last_name} failed to execute a hit and run."


def intentional_walk_rule(game_state: GameState):
    return 'walk', (f"The manager decided to intentionally walk the batter "
                    f"{game_state.batter.first_name} {game_state.batter.last_name}.")
