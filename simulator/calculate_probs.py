import random
from data_loader.player import Batter


def calculate_defensive_rate(players: list[Batter]):
    """
    Calculates the defensive rate for a list of players.

    Args:
        players (list[Batter]): A list of Batter objects representing the players.

    Returns:
        float: The calculated defensive rate.
    """
    total_defensive_metric = 0
    count = 0

    for player in players:
        if 'DH' not in player.pos and 'P' not in player.pos:
            if player.oaa:
                total_defensive_metric += player.oaa * player.ab
                count += player.ab
            elif player.arm_strength:
                total_defensive_metric += player.arm_strength
                count += 1

    if count == 0:
        return 0  # Avoid division by zero if no defensive metrics are available

    return total_defensive_metric / count


def determine_pitch_result(batter, pitcher, first_runner, pitch_count, defensive_rate, tamper_dp=0):
    """
    Determines the result of a pitch based on various factors.

    Args:
        batter (Batter): The batter facing the pitch.
        pitcher (Pitcher): The pitcher throwing the pitch.
        first_runner (Runner): The runner on first base, if any.
        pitch_count (int): The current pitch count.
        defensive_rate (float): The defensive rate of the fielding team.
        tamper_dp (float, optional): Adjustment factor for double play probability. Defaults to 0.

    Returns:
        tuple: A tuple containing the result of the pitch and the total number of pitches thrown.
    """
    strikes = 0
    balls = 0
    total_pitches = 0

    # Calculate probabilities for each pitch outcome
    strike_prob = (pitcher.k_percent + batter.k_percent) / 200
    ball_prob = (pitcher.bb_percent + batter.bb_percent) / 200
    foul_prob = 0.2  # Initial probability of a foul ball
    hit_prob = (batter.avg + pitcher.avg) / 2

    # Adjust hit probability based on defensive rate
    hit_prob *= (1 - defensive_rate / 90)

    # Increase hit probability after 70 pitches
    if pitch_count > 70:
        hit_prob *= 1.05

    # Increase the double play probability if first_runner and batter are slow players
    if first_runner:
        double_play_prob = 0.02 + tamper_dp
        if (first_runner.sprint_speed and first_runner.sprint_speed < 30 and
                batter.sprint_speed and batter.sprint_speed < 30):
            double_play_prob += 0.13
    else:
        double_play_prob = 0

    out_prob = 1 - (strike_prob + ball_prob + foul_prob + hit_prob + double_play_prob)
    outcomes = ['strike', 'ball', 'foul', 'hit', 'out', 'double_play']

    batter_single_rate = batter.single / batter.ab
    batter_double_rate = batter.double / batter.ab
    batter_triple_rate = batter.triple / batter.ab
    batter_home_run_rate = batter.home_run / batter.ab
    pitcher_single_rate = pitcher.single / pitcher.ab
    pitcher_double_rate = pitcher.double / pitcher.ab
    pitcher_triple_rate = pitcher.triple / pitcher.ab
    pitcher_home_run_rate = pitcher.home_run / pitcher.ab

    single_prob = (batter_single_rate + pitcher_single_rate) / 2
    double_prob = (batter_double_rate + pitcher_double_rate + tamper_dp) / 2
    triple_prob = (batter_triple_rate + pitcher_triple_rate) / 2
    home_run_prob = (batter_home_run_rate + pitcher_home_run_rate) / 2

    # Normalize hit probabilities
    hit_total_prob = single_prob + double_prob + triple_prob + home_run_prob
    hit_probabilities = [single_prob / hit_total_prob, double_prob / hit_total_prob, triple_prob / hit_total_prob,
                         home_run_prob / hit_total_prob]
    while True:
        total_pitches += 1

        # Normalize probabilities to sum to 1
        total_prob = strike_prob + ball_prob + foul_prob + hit_prob + out_prob + double_play_prob
        probabilities = [strike_prob / total_prob, ball_prob / total_prob, foul_prob / total_prob,
                         hit_prob / total_prob, out_prob / total_prob, double_play_prob / total_prob]

        pitch_result = random.choices(outcomes, probabilities)[0]

        if pitch_result == 'strike':
            strikes += 1
            if strikes >= 3:
                return 'strikeout', total_pitches
        elif pitch_result == 'ball':
            balls += 1
            if balls >= 4:
                return 'walk', total_pitches
        elif pitch_result == 'foul':
            # Decrease probability of a foul ball each time to prevent infinite at-bats
            foul_prob *= 0.8
            if strikes < 2:
                strikes += 1
        elif pitch_result == 'hit':
            # Determine type of hit
            hit_outcomes = ['single', 'double', 'triple', 'home_run']
            hit_result = random.choices(hit_outcomes, hit_probabilities)[0]
            return hit_result, total_pitches
        elif pitch_result == 'out':
            return 'out', total_pitches
        elif pitch_result == 'double_play':
            return 'double_play', total_pitches