import random
from simulator.game_simulator import GameSimulator
from data_loader import data_loader as dl
from data_loader.team import Team
from manager.baseball_manager import BaseballManager
from genetica.mlbeticA import get_lineup
from manager.pitcher_selection import *

def simulate_series(team1: Team, team2: Team, games, type, log_dir="logs/Series"):
    """Simulate a series of games between two teams."""
    team1_wins = 0
    team2_wins = 0
    required_wins = (games // 2) + 1
    all_games_stats = []

    for _ in range(games):
        game_simulator = simulate_game(team1, team2)

        # Collect final statistics
        game_stats = game_simulator.get_final_statistics()
        all_games_stats.append(game_stats)

        # Determine the winner of the game
        if game_simulator.get_winner() == team1.team_name:
            team1_wins += 1
        else:
            team2_wins += 1

        # Check if any team has won the required number of games
        if team1_wins == required_wins:
            return team1, all_games_stats
        elif team2_wins == required_wins:
            return team2, all_games_stats
    return random.choice([team1, team2]), all_games_stats


def simulate_game(team1, team2):
    t1_pitchers, t1_batters = dl.separate_pitchers_batters(team1)
    t2_pitchers, t2_batters = dl.separate_pitchers_batters(team2)
    
    # Get pitchers
    rotation_t1, bullpen_t1, rotation_t2, bullpen_t2 = get_rotations_bullpens(t1_pitchers, t2_pitchers)

    h_lineup = get_lineup(team1)
    a_lineup = get_lineup(team2)
    # h_lineup = [rotation_t1[0]]
    # a_lineup = [rotation_t2[0]]

    # h_lineup[0] = rotation_t1[0]
    # a_lineup[0] = rotation_t2[0]

    # Fill lineups with first 9 batters
    for i in range(10):
        h_lineup.append(t1_batters[i])
        a_lineup.append(t2_batters[i])

    game_simulator = GameSimulator(BaseballManager(), team1, team2, t1_batters, t2_batters,
                                   h_lineup, a_lineup, bullpen_t1, bullpen_t2)
    game_simulator.simulate_game()
    game_simulator.save_log()
    return game_simulator

def save_series_logs(filename, log, game_type):
    # Extract relevant information from the log
    home_team = log['Home Team']
    home_score = log['Home Score']
    away_team = log['Away Team']
    away_score = log['Away Score']

    # Convert the log into the required format
    series_log = [home_team, away_team, str(home_score), str(away_score)]
