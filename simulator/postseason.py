import json
from data_loader.team import Team


def load_final_statistics(filename='final_statistics.json'):
    """
    Load the final statistics from a JSON file.

    Parameters:
    -----------
    filename : str, optional
        The name of the JSON file containing the final statistics (default is 'final_statistics.json').

    Returns:
    --------
    dict
        The final statistics loaded from the JSON file.
    """
    with open(filename, 'r') as f:
        return json.load(f)


def calculate_win_loss(records, final_statistics):
    """
    Calculate the win-loss records for each team based on the final statistics.

    Parameters:
    -----------
    records : dict
        A dictionary to store the win-loss records for each team.
    final_statistics : list
        A list of dictionaries containing the final statistics for each game.
    """
    for game in final_statistics:
        home_team = game["Home Team"]
        away_team = game["Away Team"]
        home_score = game["Home Score"]
        away_score = game["Away Score"]

        if home_score > away_score:
            records[home_team]["wins"] += 1
            records[away_team]["losses"] += 1
        else:
            records[home_team]["losses"] += 1
            records[away_team]["wins"] += 1


def select_best_teams(records, teams):
    """
    Select the best teams from each division based on their win-loss records.

    Parameters:
    -----------
    records : dict
        A dictionary containing the win-loss records for each team.
    teams : list
        A list of Team objects representing all the teams.

    Returns:
    --------
    dict
        A dictionary containing the best team from each division.
    """
    best_teams = {}
    for team in teams:
        division_id = team.division
        if division_id not in best_teams or records[team.team_name]["wins"] > records[best_teams[division_id]]["wins"]:
            best_teams[division_id] = team.team_name
    return best_teams


def select_wild_card_teams(teams: list[Team], division_winners, records, num_wild_cards=3):
    """
    Select the wild card teams based on their win-loss records.

    Parameters:
    -----------
    teams : list[Team]
        A list of Team objects representing all the teams.
    division_winners : list
        A list of team names that won their divisions.
    records : dict
        A dictionary containing the win-loss records for each team.
    num_wild_cards : int, optional
        The number of wild card teams to select (default is 3).

    Returns:
    --------
    list
        A list of team names representing the wild card teams.
    """
    non_division_winners = [team for team in teams if team not in division_winners]
    non_division_winners = sorted(non_division_winners, key=lambda team: records[team]["wins"], reverse=True)
    return non_division_winners[:num_wild_cards]


def get_postseason_teams(teams: list[Team]):
    """
    Get the teams that made it to the postseason.

    Parameters:
    -----------
    teams : list[Team]
        A list of Team objects representing all the teams.

    Returns:
    --------
    tuple
        A tuple containing two lists: the AL postseason teams and the NL postseason teams.
    """
    # Load final statistics
    final_statistics = load_final_statistics()

    # Initialize win-loss records
    records = {team.team_name: {"wins": 0, "losses": 0} for team in teams}

    # Calculate win-loss records
    calculate_win_loss(records, final_statistics)

    # Select the best teams from each division
    division_winners = select_best_teams(records, teams)

    # Get AL, NL teams
    al_teams = [team.team_name for team in teams if team.league == "AL"]
    nl_teams = [team.team_name for team in teams if team.league == "NL"]

    # Get AL, NL division winners
    al_division_winners = [team for team in al_teams if team in division_winners.values()]
    nl_division_winners = [team for team in nl_teams if team in division_winners.values()]

    # Select wild card teams
    al_wild_card_teams = select_wild_card_teams(al_teams, al_division_winners, records)
    nl_wild_card_teams = select_wild_card_teams(nl_teams, nl_division_winners, records)

    # Combine division winners and wild card teams
    al_postseason_teams = al_division_winners + al_wild_card_teams
    nl_postseason_teams = nl_division_winners + nl_wild_card_teams

    # return original teams:
    al_postseason_teams = [team for team in teams if team.team_name in al_postseason_teams]
    nl_postseason_teams = [team for team in teams if team.team_name in nl_postseason_teams]

    return al_postseason_teams, nl_postseason_teams