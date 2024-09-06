import random
import statsapi
from player import Batter, Pitcher
from team import Team


def get_teams(batters, pitchers):
    # Get all teams from statsapi
    teams = statsapi.get('teams', {'sportId': 1})
    team_ids_names = [(team['id'], team['name']) for team in teams['teams']]

    teams = []
    # Get players and positions for each team
    for team_id, team_name in team_ids_names:
        roster = statsapi.get('team_roster', {'teamId': team_id})
        # print(f"Team ID: {team_id}, Name: {team_name}")
        team_players = []
        for player in roster['roster']:
            print(f"Player: {player['person']['fullName']}, Position: {player['position']['abbreviation']}")
            team_players.append((player['person']['fullName'], player['position']['abbreviation']))

        teams.append([team_id, team_name, team_players, []])

    # teams actual format is not useful for simulation. Need to identify players according to their names and get
    # their stats

    # SEARCHING players and grouping by team
    real_teams = []
    for t in teams:
        for p in t[2]:
            founded = False
            for _, row in batters.iterrows():
                if p[0] == row['last_name, first_name']:
                    player = Batter(row)
                    t[3].append(player)
                    founded = True
                    break

            if founded:
                break

            for _, row in pitchers.iterrows():
                if p[0] == row['last_name, first_name']:
                    player = Pitcher(row)
                    t[3].append(player)
                    break

    for t in teams:
        real_teams.append(Team(t[0], t[1], t[3]))

    return real_teams


def fitness_lineup(team):
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

# def random_population(self, size):
#     population = []
#     for  _ in range(size):
#         team = random.sample(self.batters, k=8) + random.sample(self.pitchers, k=1)
#         population.append(team)
#
#     return population """
#
# (self, last_name_first_name, player_id, year, p_game, pa, ab, hit, single, double, triple, home_run, strikeout,
# walk, k_percent, bb_percent, batting_avg, slg_percent, on_base_percent, on_base_plus_slg, woba, xwoba,
# sweet_spot_percent, barrel_batted_rate, hard_hit_percent, avg_best_speed, avg_hyper_speed, whiff_percent,
# swing_percent, pitch_hand) """
