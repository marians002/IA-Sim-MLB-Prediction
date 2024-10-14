import pandas as pd
from simulator.series_simulator import *


def save_final_statistics(schedule, filename='final_statistics.json'):
    all_game_stats = []

    for game in schedule:
        print("Simulating game: ", game[0].team_name, " vs. ", game[1].team_name)
        game_simulator = simulate_game(game[0], game[1])

        # Collect final statistics
        game_stats = game_simulator.get_final_statistics()
        all_game_stats.append(game_stats)

    # Save all game statistics to a JSON file
    with open(filename, 'w') as f:
        json.dump(all_game_stats, f, indent=4)

    return all_game_stats


def create_dataframes_from_results(results):
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

        if league == 'NL':
            nl_overall_data.append(team_data)
            nl_divisions[division].append(team_data)
        elif league == 'AL':
            al_overall_data.append(team_data)
            al_divisions[division].append(team_data)

    # Sort the lists by victories
    nl_east_data = sorted(nl_east_data, key=lambda x: x['Victories'], reverse=True)
    nl_west_data = sorted(nl_west_data, key=lambda x: x['Victories'], reverse=True)
    nl_central_data = sorted(nl_central_data, key=lambda x: x['Victories'], reverse=True)
    nl_overall_data = sorted(nl_overall_data, key=lambda x: x['Victories'], reverse=True)

    al_east_data = sorted(al_east_data, key=lambda x: x['Victories'], reverse=True)
    al_west_data = sorted(al_west_data, key=lambda x: x['Victories'], reverse=True)
    al_central_data = sorted(al_central_data, key=lambda x: x['Victories'], reverse=True)
    al_overall_data = sorted(al_overall_data, key=lambda x: x['Victories'], reverse=True)

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
