import pandas as pd

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
        league, division = get_league_and_division(team)
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

def get_league_and_division(team_name):
         # Define the divisions
        if team_name in ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays", "Toronto Blue Jays"]:
            return "AL", "AL East"
        elif team_name in ["Chicago White Sox", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"]:
            return "AL", "AL Central"
        elif team_name in ["Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners", "Texas Rangers"]:
            return "AL", "AL West"
        elif team_name in ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies", "Washington Nationals"]:
            return "NL", "NL East"
        elif team_name in ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates", "St. Louis Cardinals"]:
            return "NL", "NL Central"
        elif team_name in ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres", "San Francisco Giants"]:
            return "NL", "NL West"
        else:
            raise Exception("Team not found in any division")