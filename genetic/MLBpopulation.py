import statsapi
from player import Batter, Pitcher
from team import Team

def name_formatter(last_name_first_name):
    """ Returning a string of the form: FIRST_NAME LAST_NAME, for a matter of using same format in both datasets"""
    for i in range(len(last_name_first_name)):
        if last_name_first_name[i] == ',':
            return last_name_first_name[i+2:] + ' ' + last_name_first_name[:i]
        
        

def get_teams(batters, pitchers):
    # Get all teams from statsapi
    teams = statsapi.get('teams', {'sportId': 1})
    team_ids_names = [(team['id'], team['name']) for team in teams['teams']]

    teams = []
    # Get players and positions for each team
    for team_id, team_name in team_ids_names:
        roster = statsapi.get('team_roster', {'teamId': team_id})
        team_players = []
        for player in roster['roster']:
            team_players.append((player['person']['fullName'], player['position']['abbreviation']))
        
        # fourth position is reserved for a list of Player class objects
        teams.append([team_id, team_name, team_players, []])

    # teams actual format is not useful for simulation. Need to identify players according to their names and get their stats
    
    # SEARCHING players and groupping by team
    real_teams = []
    for t in teams:
        for p in t[2]:
            founded = False
            for _, row in batters.iterrows():
                if p[0] == name_formatter(row['last_name, first_name']):
                    player = Batter(list(row), pos=[p[1]])
                    t[3].append(player)
                    founded = True
                    break

            if founded:
                break

            for _, row in pitchers.iterrows():
                if p[0] == name_formatter(row['last_name, first_name']):
                    player = Pitcher(list(row), pos=[p[1], 'P'])
                    t[3].append(player)
                    break

    for t in teams:
        real_teams.append(Team(t[0], t[1], t[3]))

    return real_teams


def fitness_lineup(team):
    """ Simple fitness func for Players """
    val = 0
    val += team[0].on_base_percent * 0.5 + team[0].avg_best_speed * 0.3 + team[0].batting_avg * 0.2
    val += team[1].on_base_percent * 0.5 + team[1].avg_best_speed * 0.3 + team[1].batting_avg * 0.2
    val += team[2].on_base_percent * 0.5 + team[2].avg_best_speed * 0.3 + team[2].batting_avg * 0.2
    val += team[3].on_base_percent * 0.5 + team[3].avg_best_speed * 0.3 + team[3].batting_avg * 0.2
    val += team[4].on_base_percent * 0.5 + team[4].avg_best_speed * 0.3 + team[4].batting_avg * 0.2
    val += team[5].on_base_percent * 0.5 + team[5].avg_best_speed * 0.3 + team[5].batting_avg * 0.2
    val += team[6].on_base_percent * 0.5 + team[6].avg_best_speed * 0.3 + team[6].batting_avg * 0.2
    val += team[7].on_base_percent * 0.5 + team[7].avg_best_speed * 0.3 + team[7].batting_avg * 0.2
    val += team[8].on_base_percent * 0.5 + team[8].avg_best_speed * 0.3 + team[8].batting_avg * 0.2

    return val