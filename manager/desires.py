def conservative_manager(game_state):
    conditions = [
        game_state.inning >= 7,
        game_state.score_difference <= 2,
        game_state.pitch_count_home > 90,
        game_state.outs >= 2
    ]
    return sum(conditions)


def aggressive_manager(game_state):
    conditions = [
        game_state.inning < 7,
        game_state.score_difference < 0,
        game_state.runner_on_first is not None,
        game_state.outs < 2
    ]
    return sum(conditions)


def defensive_manager(game_state):
    conditions = [
        game_state.inning >= 7,
        game_state.score_difference > 2,
        game_state.runner_on_first is not None,
        game_state.outs >= 2
    ]
    return sum(conditions)


def neutral_manager():
    conditions = [
        True  # Neutral manager has no specific conditions
    ]
    return sum(conditions)


def evaluate_manager_types(game_state):
    # Calculate the number of conditions met for each manager type
    conservative_met = conservative_manager(game_state)
    aggressive_met = aggressive_manager(game_state)
    defensive_met = defensive_manager(game_state)
    neutral_met = neutral_manager()

    # Calculate the total number of conditions
    total_conditions = 2

    # Calculate the percentage of each manager type
    conservative_percentage = (conservative_met / total_conditions) * 100
    aggressive_percentage = (aggressive_met / total_conditions) * 100
    defensive_percentage = (defensive_met / total_conditions) * 100
    neutral_percentage = (neutral_met / total_conditions) * 100

    # Normalize percentages
    total_percentage = conservative_percentage + aggressive_percentage + defensive_percentage + neutral_percentage
    conservative_percentage = (conservative_percentage / total_percentage) * 100
    aggressive_percentage = (aggressive_percentage / total_percentage) * 100
    defensive_percentage = (defensive_percentage / total_percentage) * 100
    neutral_percentage = (neutral_percentage / total_percentage) * 100

    return {
        "conservative": conservative_percentage,
        "aggressive": aggressive_percentage,
        "defensive": defensive_percentage,
        "neutral": neutral_percentage
    }
