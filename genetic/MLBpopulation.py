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
                    player = Batter(
                        last_name_first_name=row['last_name, first_name'],
                        player_id=row['player_id'],
                        year=row['year'],
                        p_game=row['p_game'],
                        pa=row['pa'],
                        ab=row['ab'],
                        hit=row['hit'],
                        single=row['single'],
                        double=row['double'],
                        triple=row['triple'],
                        home_run=row['home_run'],
                        strikeout=row['strikeout'],
                        walk=row['walk'],
                        k_percent=row['k_percent'],
                        bb_percent=row['bb_percent'],
                        batting_avg=row['batting_avg'],
                        slg_percent=row['slg_percent'],
                        on_base_percent=row['on_base_percent'],
                        on_base_plus_slg=row['on_base_plus_slg'],
                        woba=row['woba'],
                        xwoba=row['xwoba'],
                        sweet_spot_percent=row['sweet_spot_percent'],
                        barrel_batted_rate=row['barrel_batted_rate'],
                        hard_hit_percent=row['hard_hit_percent'],
                        avg_best_speed=row['avg_best_speed'],
                        avg_hyper_speed=row['avg_hyper_speed'],
                        whiff_percent=row['whiff_percent'],
                        swing_percent=row['swing_percent'],
                        pitch_hand=row['pitch_hand']
                    )
                    t[3].append(player)
                    founded = True
                    break

            if founded:
                break

            for _, row in pitchers.iterrows():
                if p[0] == row['last_name, first_name']:
                    player = Pitcher(
                        last_name_first_name=row['last_name, first_name'],
                        player_id=row['player_id'],
                        year=row['year'],
                        p_game=row['p_game'],
                        pitch_hand=row['pitch_hand'],
                        ip=row['ip'],
                        era=row['era'],
                        whip=row['whip'],
                        k_9=row['k_9'],
                        bb_9=row['bb_9'],
                        hr_9=row['hr_9'],
                        fip=row['fip'],
                        xfip=row['xfip'],
                        k_percent=row['k_percent'],
                        bb_percent=row['bb_percent'],
                        ground_ball_percent=row['ground_ball_percent'],
                        fly_ball_percent=row['fly_ball_percent'],
                        line_drive_percent=row['line_drive_percent'],
                        soft_contact_percent=row['soft_contact_percent'],
                        medium_contact_percent=row['medium_contact_percent'],
                        hard_contact_percent=row['hard_contact_percent']
                    )
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
