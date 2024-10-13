# pitcher_selection.py

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


# Example usage
if __name__ == "__main__":
    # Assume we have a list of Pitcher objects
    pitchers = [...]  # List of Pitcher objects
    rotation = select_starting_pitchers(pitchers)
    for pitcher in rotation:
        print(pitcher)
