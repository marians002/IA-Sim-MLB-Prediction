import os, json, random
from simulator.game_simulator import GameSimulator
from data_loader import data_loader as dl
from data_loader.team import Team
from manager.baseball_manager import BaseballManager

def simulate_series(team1: Team, team2: Team, games, type, log_dir="logs/Series"):
    """Simulate a series of games between two teams."""
    team1_wins = 0
    team2_wins = 0
    required_wins = (games // 2) + 1

    for _ in range(games):
        game_simulator = simulate_game(team1, team2)
        
        stats = game_simulator.get_final_statistics()
        
        # Determine the winner of the game
        if game_simulator.get_winner() == team1.team_name:
            
            team1_wins += 1
        else:
            team2_wins += 1

        # Check if any team has won the required number of games
        if team1_wins == required_wins:
            return team1
        elif team2_wins == required_wins:
            return team2

    # In case of a tie, randomly select a winner (this should not happen in a real series)
    return random.choice([team1, team2])

def simulate_game(team1, team2):
    t1_pitchers, t1_batters = dl.separate_pitchers_batters(team1)
    t2_pitchers, t2_batters = dl.separate_pitchers_batters(team2)

    manager_t1 = BaseballManager()
    manager_t2 = BaseballManager()

    h_lineup = [t1_pitchers[0]]
    t1_pitchers.pop(0)  # Remove the opening pitcher from the bullpen
    a_lineup = [t2_pitchers[0]]
    t2_pitchers.pop(0)  # Remove the opening pitcher from the bullpen

    for i in range(10):
        h_lineup.append(t1_batters[i])
        a_lineup.append(t2_batters[i])

    game_simulator = GameSimulator(manager_t1, manager_t2, team1, team2, t1_batters, t1_pitchers, t2_batters, t2_pitchers,
                                    h_lineup, a_lineup)
    game_simulator.simulate_game()
    game_simulator.save_log()
    return game_simulator

import json
import os

def save_series_logs(filename, log, game_type):
    # Extract relevant information from the log
    home_team = log['Home Team']
    home_score = log['Home Score']
    away_team = log['Away Team']
    away_score = log['Away Score']

    # Convert the log into the required format
    series_log = [home_team, away_team, str(home_score), str(away_score)]
