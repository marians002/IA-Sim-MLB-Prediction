from data_loader.player import Pitcher


def calculate_pitcher_score(pitcher: Pitcher):
    """
    Calculate the score of a pitcher based on various performance metrics.

    The score is calculated using the following formula:
        score = (avg_best_speed * 0.2) + (whiff_percent * 0.3) + (strikeout * 0.25) - (walk * 0.15)

    Args:
        pitcher (Pitcher): An instance of the Pitcher class containing the following attributes:
            avg_best_speed (float): The average best speed of the pitcher.
            whiff_percent (float): The percentage of swings and misses.
            strikeout (int): The number of strikeouts.
            walk (int): The number of walks.

    Returns:
        float: The calculated score of the pitcher.
    """
    score = (
            pitcher.avg_best_speed * 0.2 +
            pitcher.whiff_percent * 0.3 +
            pitcher.strikeout * 0.25 -
            pitcher.walk * 0.15
    )
    return score


def select_starting_pitchers(pitchers, rotation_size=5):
    """
    Selects the top starting pitchers based on their calculated scores.

    Args:
        pitchers (list): A list of pitcher objects or dictionaries containing pitcher data.
        rotation_size (int, optional): The number of pitchers to include in the starting rotation. Defaults to 5.

    Returns:
        list: A list of the top N pitchers selected for the starting rotation.
    """
    # Calculate scores for each pitcher
    pitcher_scores = [(p, calculate_pitcher_score(p)) for p in pitchers]

    # Sort pitchers by score in descending order
    sorted_pitchers = sorted(pitcher_scores, key=lambda x: x[1], reverse=True)

    # Select the top N pitchers for the rotation
    starting_rotation = [p for p, score in sorted_pitchers[:rotation_size]]

    return starting_rotation


def bullpen_management(starters, all_pitchers):
    """
    Manages the bullpen by selecting the top pitchers based on their calculated scores.

    Args:
        starters (list): A list of starting pitchers.
        all_pitchers (list): A list of all available pitchers.

    Returns:
        list: A list of the top pitchers sorted by their scores in descending order.
    """
    # Calculate scores for each pitcher
    pitchers = [p for p in all_pitchers if p not in starters]
    pitcher_scores = [(p, calculate_pitcher_score(p)) for p in pitchers]

    # Sort pitchers by score in descending order
    sorted_pitchers = sorted(pitcher_scores, key=lambda x: x[1], reverse=True)

    # Select the top N pitchers for the rotation
    return [p for p, score in sorted_pitchers]


def get_rotations_bullpens(t1_pitchers, t2_pitchers, rot_t1=0, rot_t2=0):
    """
    Determines the starting rotations and bullpens for two teams of pitchers.

    Args:
        t1_pitchers (list): A list of pitchers for team 1.
        t2_pitchers (list): A list of pitchers for team 2.
        rot_t1 (int, optional): The current rotation index for team 1. Defaults to 0.
        rot_t2 (int, optional): The current rotation index for team 2. Defaults to 0.

    Returns:
        tuple: A tuple containing four elements:
            - rotation_t1 (list): The starting rotation for team 1.
            - bullpen_t1 (list): The bullpen for team 1.
            - rotation_t2 (list): The starting rotation for team 2.
            - bullpen_t2 (list): The bullpen for team 2.
    """
    rotation_t1 = select_starting_pitchers(t1_pitchers)
    bullpen_t1 = bullpen_management(rotation_t1, t1_pitchers)

    rotation_t2 = select_starting_pitchers(t2_pitchers)
    bullpen_t2 = bullpen_management(rotation_t2, t2_pitchers)

    starter_t1 = rotation_t1[rot_t1 % len(rotation_t1)]
    starter_t2 = rotation_t2[rot_t2 % len(rotation_t2)]

    return rotation_t1, bullpen_t1, rotation_t2, bullpen_t2, starter_t1, starter_t2
