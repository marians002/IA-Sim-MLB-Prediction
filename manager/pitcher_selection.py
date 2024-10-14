from data_loader.player import Pitcher


def calculate_pitcher_score(pitcher: Pitcher):
    # Example scoring function, adjust weights as needed
    score = (
            pitcher.avg_best_speed * 0.2 +
            pitcher.whiff_percent * 0.3 +
            pitcher.strikeout * 0.25 -
            pitcher.walk * 0.15
    )
    return score


def select_starting_pitchers(pitchers, rotation_size=5):
    # Calculate scores for each pitcher
    pitcher_scores = [(p, calculate_pitcher_score(p)) for p in pitchers]

    # Sort pitchers by score in descending order
    sorted_pitchers = sorted(pitcher_scores, key=lambda x: x[1], reverse=True)

    # Select the top N pitchers for the rotation
    starting_rotation = [p for p, score in sorted_pitchers[:rotation_size]]

    return starting_rotation


def bullpen_management(starters, all_pitchers):
    # Calculate scores for each pitcher
    pitchers = [p for p in all_pitchers if p not in starters]
    pitcher_scores = [(p, calculate_pitcher_score(p)) for p in pitchers]

    # Sort pitchers by score in descending order
    sorted_pitchers = sorted(pitcher_scores, key=lambda x: x[1], reverse=True)

    # Select the top N pitchers for the rotation
    return [p for p, score in sorted_pitchers]


def get_rotations_bullpens(t1_pitchers, t2_pitchers):
    rotation_t1 = select_starting_pitchers(t1_pitchers)
    bullpen_t1 = bullpen_management(rotation_t1, t1_pitchers)

    rotation_t2 = select_starting_pitchers(t2_pitchers)
    bullpen_t2 = bullpen_management(rotation_t2, t2_pitchers)

    return rotation_t1, bullpen_t1, rotation_t2, bullpen_t2
