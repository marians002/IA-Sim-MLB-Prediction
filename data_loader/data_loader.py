import json
import os
import statsapi

import pandas as pd

from data_loader.player import *
from data_loader.team import Team


# Fill the players list
def get_players(data, players, type_batter):
    for _, row in data.iterrows():
        first_name, last_name = name_formatter(row['last_name, first_name'])
        player_data = [first_name, last_name] + list(row)[1:]
        if type_batter:
            players.append(Batter(player_data))
        else:
            players.append(Pitcher(player_data))


# Split the names of players in the first column
def name_formatter(last_name_first_name):
    # Split the string at the comma
    comma_index = last_name_first_name.index(',')
    first_name = last_name_first_name[comma_index + 2:]
    last_name = last_name_first_name[:comma_index]

    # Return the formatted string
    return first_name, last_name


def get_team_rosters(year=2022):
    # Get all teams from statsapi
    teams_data = statsapi.get('teams', {'sportId': 1})
    team_ids_names = [(team['id'], team['name']) for team in teams_data['teams']]

    team_rosters = {}
    for team_id, team_name in team_ids_names:
        # Get the roster for each team
        roster = statsapi.get('team_roster', {'teamId': team_id, 'season': year})
        team_players = []
        for player in roster['roster']:
            player_name = player['person']['fullName']
            player_position = player['position']['abbreviation']
            team_players.append((player_name, player_position))

        team_rosters[team_name] = team_players

    return team_rosters


def add_players_to_teams(team_rosters, players):
    teams = []

    for team_name, team_players in team_rosters.items():
        new_team = Team(team_name)
        for player_name, player_position in team_players:
            for player in players:
                if player.first_name + ' ' + player.last_name == player_name:
                    player.pos = [player_position]
                    new_team.add_player(player)
                    break
        teams.append(new_team)

    return teams


def print_team_rosters(team_rosters):
    for team in team_rosters:
        print(f"Team: {team['team_name']}")
        for player in team['players']:
            print(f"  Player: {player['first_name'] + ' ' + player['last_name']}, Position: {player['pos']}")
        print()


def load_csv():
    # Get the path to the CSV file
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, '../stats csv', 'pitchers 2022 PA50.csv')
    pitchers = pd.read_csv(csv_path)
    csv_path = os.path.join(current_dir, '../stats csv', 'batters 2022 PA50.csv')
    batters = pd.read_csv(csv_path)
    return pitchers, batters


def get_teams():
    pitchers, batters = load_csv()

    # Create a list of Batter objects from the batters DataFrame
    players = []
    get_players(pitchers, players, False)
    get_players(batters, players, True)

    # Retrieve team rosters from statsapi
    team_rosters = get_team_rosters(year=2022)

    # Add players to teams
    teams = add_players_to_teams(team_rosters, players)

    return teams, players


def load_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_data():
    teams_file = 'teams.json'
    players_file = 'players.json'

    if os.path.exists(teams_file) and os.path.exists(players_file):
        # Load teams and players from JSON files
        teams_dict = load_from_json(teams_file)
        players_dict = load_from_json(players_file)
    else:
        # Load teams and players
        teams, players = get_teams()

        # Convert teams and players to dictionaries
        teams_dict = [team.to_dict() for team in teams]
        players_dict = [player.to_dict() for player in players]

        # Save teams and players to JSON files
        save_to_json(teams_dict, teams_file)
        save_to_json(players_dict, players_file)

    # print_team_rosters(teams_dict)
    print("Teams and players data loaded successfully.")
    return teams_dict, players_dict
