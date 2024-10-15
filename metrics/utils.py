import pandas as pd
import json, os
from simulator.series_simulator import *

def save_final_statistics(schedule, filename='final_statistics.json', verbose=False):
    """
    Simulates a series of games, collects their final statistics, and saves them to a JSON file.

    Args:
        schedule (list): A list of tuples, where each tuple contains two teams to be simulated.
        filename (str, optional): The name of the JSON file where the final statistics will be saved. Defaults to 'final_statistics.json'.
        verbose (bool, optional): If True, prints the progress of the game simulations. Defaults to False.

    Returns:
        list: A list of dictionaries containing the final statistics for each game.
    """
    all_games_stats = []
    rotations = {}

    for game in schedule:
        if verbose:
            print("\033[91mSimulating game:\033[0m ", game[0].team_name, " vs. ", game[1].team_name)

        if game[0] not in rotations:
            rotations[game[0]] = 0
        else:
            rotations[game[0]] += 1
        if game[1] not in rotations:
            rotations[game[1]] = 0
        else:
            rotations[game[1]] += 1

        game_simulator = simulate_game(game[0], game[1], rotations[game[0]], rotations[game[1]])

        # Collect final statistics
        game_stats = game_simulator.get_final_statistics()
        all_games_stats.append(game_stats)

    # Save all game statistics to a JSON file
    with open(filename, 'w') as f:
        json.dump(all_games_stats, f, indent=4)

    print("\033[92mSeason is over. All games simulated\033[0m")
    return all_games_stats


def create_dataframes_from_results(results, teams):
    """
    Create DataFrames from game results and team information.

    This function processes a list of game results and a list of team objects to generate
    DataFrames for each division and league in Major League Baseball (MLB). The DataFrames
    contain information about each team's victories, losses, and position within their
    respective divisions and leagues.

    Parameters:
    results (list of dict): A list of dictionaries where each dictionary represents a game result.
                            Each dictionary should have the following keys:
                            - 'Home Team': Name of the home team (str)
                            - 'Home Score': Score of the home team (int)
                            - 'Away Team': Name of the away team (str)
                            - 'Away Score': Score of the away team (int)
    teams (list of objects): A list of team objects. Each object should have the following attributes:
                             - team_name (str): Name of the team
                             - league (str): League of the team ('NL' or 'AL')
                             - division (str): Division of the team ('NL East', 'NL West', 'NL Central',
                                               'AL East', 'AL West', 'AL Central')

    Returns:
    tuple: A tuple containing eight pandas DataFrames in the following order:
           - nl_east_df: DataFrame for National League East division
           - nl_west_df: DataFrame for National League West division
           - nl_central_df: DataFrame for National League Central division
           - nl_overall_df: DataFrame for overall National League
           - al_east_df: DataFrame for American League East division
           - al_west_df: DataFrame for American League West division
           - al_central_df: DataFrame for American League Central division
           - al_overall_df: DataFrame for overall American League
    """
    # Initialize empty dictionaries for victories and losses
    victories = {}
    losses = {}

    # Iterate through the results and update victories and losses
    for result in results:
        home_team = result['Home Team']
        home_score = result['Home Score']
        away_team = result['Away Team']
        away_score = result['Away Score']

        if home_team not in victories:
            victories[home_team] = 0
            losses[home_team] = 0
        if away_team not in victories:
            victories[away_team] = 0
            losses[away_team] = 0

        if home_score > away_score:
            victories[home_team] += 1
            losses[away_team] += 1
        else:
            victories[away_team] += 1
            losses[home_team] += 1

    # Create lists for each division and league
    nl_east_data = []
    nl_west_data = []
    nl_central_data = []
    nl_overall_data = []

    al_east_data = []
    al_west_data = []
    al_central_data = []
    al_overall_data = []

    # Define the divisions for each league
    nl_divisions = {
        'NL East': nl_east_data,
        'NL West': nl_west_data,
        'NL Central': nl_central_data
    }

    al_divisions = {
        'AL East': al_east_data,
        'AL West': al_west_data,
        'AL Central': al_central_data
    }

    # Populate the lists with team data
    for team, wins in victories.items():
        team_data = {'Team': team, 'Victories': wins, 'Losses': losses[team]}
        t = None
        for team_obj in teams:
            if team_obj.team_name == team:
                t = team_obj
                break

        if t.league == 'NL':
            nl_overall_data.append(team_data)
            nl_divisions[t.division].append(team_data)
        elif t.league == 'AL':
            al_overall_data.append(team_data)
            al_divisions[t.division].append(team_data)

    # Sort the lists by victories
    for data in [nl_east_data, nl_west_data, nl_central_data, nl_overall_data,
                 al_east_data, al_west_data, al_central_data, al_overall_data]:
        data.sort(key=lambda x: x['Victories'], reverse=True)

    # Create a column for positions
    for data in [nl_east_data, nl_west_data, nl_central_data, nl_overall_data,
                 al_east_data, al_west_data, al_central_data, al_overall_data]:
        for i, team_data in enumerate(data):
            team_data['Position'] = i + 1

    # Create DataFrames for each division and league
    nl_east_df = pd.DataFrame(nl_east_data)
    nl_west_df = pd.DataFrame(nl_west_data)
    nl_central_df = pd.DataFrame(nl_central_data)
    nl_overall_df = pd.DataFrame(nl_overall_data)

    al_east_df = pd.DataFrame(al_east_data)
    al_west_df = pd.DataFrame(al_west_data)
    al_central_df = pd.DataFrame(al_central_data)
    al_overall_df = pd.DataFrame(al_overall_data)

    return nl_east_df, nl_west_df, nl_central_df, nl_overall_df, al_east_df, al_west_df, al_central_df, al_overall_df


def load_databases():
    """
    Load and preprocess baseball division data from CSV files.

    This function reads CSV files containing data for various baseball divisions,
    adds a 'Position' column to each DataFrame, and returns the DataFrames.

    Returns:
        tuple: A tuple containing the following DataFrames:
            - nl_overall_df_original (pd.DataFrame): National League overall data.
            - al_overall_df_original (pd.DataFrame): American League overall data.
            - nl_central_df_original (pd.DataFrame): National League Central Division data.
            - nl_east_df_original (pd.DataFrame): National League East Division data.
            - nl_west_df_original (pd.DataFrame): National League West Division data.
            - al_central_df_original (pd.DataFrame): American League Central Division data.
            - al_east_df_original (pd.DataFrame): American League East Division data.
            - al_west_df_original (pd.DataFrame): American League West Division data.
    """
    # Load the original CSV data
    # get current path
    current_dir = os.path.dirname(__file__)
    path = '../data_loader/database/'
    nl_overall_df_original = pd.read_csv(os.path.join(current_dir, path, 'NL_overall.csv'))
    nl_central_df_original = pd.read_csv(os.path.join(current_dir, path, 'NL_central_division.csv'))
    nl_east_df_original = pd.read_csv(os.path.join(current_dir, path, 'NL_east_division.csv'))
    nl_west_df_original = pd.read_csv(os.path.join(current_dir, path, 'NL_west_division.csv'))
    al_overall_df_original = pd.read_csv(os.path.join(current_dir, path, 'AL_overall.csv'))
    al_central_df_original = pd.read_csv(os.path.join(current_dir, path, 'AL_central_division.csv'))
    al_east_df_original = pd.read_csv(os.path.join(current_dir, path, 'AL_east_division.csv'))
    al_west_df_original = pd.read_csv(os.path.join(current_dir, path, 'AL_west_division.csv'))

    # Add a positions column to the original DataFrames
    for df in [nl_overall_df_original, nl_central_df_original, nl_east_df_original, nl_west_df_original,
               al_overall_df_original, al_central_df_original, al_east_df_original, al_west_df_original]:
        df['Position'] = range(1, len(df) + 1)

    return (nl_overall_df_original, al_overall_df_original, nl_central_df_original, nl_east_df_original,
            nl_west_df_original, al_central_df_original, al_east_df_original, al_west_df_original)
