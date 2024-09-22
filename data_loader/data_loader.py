import os
import statsapi
import jsonpickle

import pandas as pd

from data_loader.player import *
from data_loader.team import Team


def print_players(team):
    for player in team.players:
        print(f" \033[91m Player:\033[0m {player.first_name + ' ' + player.last_name}, Position: {player.pos}")


def print_team_rosters(team_rosters):
    for team in team_rosters:
        print("\033[96mTeam: \033[0m" + team.team_name)
        print_players(team)
        print()


def load_csv():
    # Get the path to the CSV file
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, '../stats csv', 'pitchers 2022 PA50.csv')
    pitchers = pd.read_csv(csv_path).drop('year', axis=1)
    csv_path = os.path.join(current_dir, '../stats csv', 'batters 2022 PA50.csv')
    batters = pd.read_csv(csv_path).drop(['year', 'player_age'], axis=1)
    return pitchers, batters


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


def save_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json_data = jsonpickle.encode(data)
        file.write(json_data)


def load_from_json(file_path):
    with open(file_path, 'r') as file:
        json_data = file.read()
        return jsonpickle.decode(json_data)


def separate_pitchers_batters(team):
    pitchers = [player for player in team.players if isinstance(player, Pitcher)]
    batters = [player for player in team.players if isinstance(player, Batter)]
    return pitchers, batters


def load_data():
    teams_file = 'teams.json'
    players_file = 'players.json'

    if os.path.exists(teams_file) and os.path.exists(players_file):
        # Load teams and players from JSON files
        teams = load_from_json(teams_file)
        players = load_from_json(players_file)
    else:
        # Load teams and players
        teams, players = get_teams()

        # Save teams and players to JSON files
        save_to_json(teams, teams_file)
        save_to_json(players, players_file)

    print("\033[92mTeams and players data loaded successfully.\033[0m")
    print()
    return teams
