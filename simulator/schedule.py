import random, json
from simulator.series_simulator import simulate_series
from data_loader.team import Team

def generate_schedule(teams : list[Team]):
    """
    Generate the MLB schedule for 2022 without dates.
    
    Args:
    teams (list): List of Team objects.
    geographic_rivals (dict): Dictionary mapping team names to their geographic rivals.
    
    Returns:
    list: List of tuples (home, away) where home and away are Team objects.
    """
    schedule = []

    # Create a dictionary to map team names to Team objects
    team_dict = {team.team_name: team for team in teams}

    # Generate division matchups (13 games each)
    divisions = {}
    for team in teams:
        if team.division not in divisions:
            divisions[team.division] = []
        divisions[team.division].append(team)

    for division_teams in divisions.values():
        for i, team1 in enumerate(division_teams):
            for team2 in division_teams[i+1:]:
                k = random.randint(0, 1)
                schedule.extend([(team1, team2)] * (6 + k))  
                schedule.extend([(team2, team1)] * (7 - k))
            
    # Generate league matchups (6 games to 6 teams and 7 games to the remainding 4 teams for each team in league)
    al_teams = [team for team in teams if team.league == 'AL']
    nl_teams = [team for team in teams if team.league == 'NL']
    leagues = [al_teams, nl_teams]

    for league_teams in leagues:
        for i, team in enumerate(league_teams):
            opponents = [t for t in league_teams if t.division != team.division]
            for opponent in opponents:
                schedule.append((team, opponent))
                schedule.extend([(opponent , team)] * 2)

    # Generate geographic rival matchups (4 games each)
    for team in teams:
        schedule.extend([(team, team_dict[team.geographic_rival])] * 2)  # 2 home games for team
        
    # Generate interleague matchups (3 games each for 15 pairs)
    for team1 in nl_teams:
        for team2 in al_teams:
            schedule.extend([(team1, team2)] * 2 )  
            schedule.extend([(team2, team1)] * 2)
    return schedule

def create_postseason_structure(nl_teams, al_teams):
    all_stats = []
    nl_champion, stats = postseason_round(nl_teams)
    all_stats.append(stats)
    al_champion, stats = postseason_round(al_teams)
    all_stats.append(stats)

    world_series_winner, stats = simulate_series(nl_champion, al_champion, 7, "World Series", "logs/World Series")
    all_stats.append(stats)

    # Save all game statistics to a JSON file
    with open('postseason.json', 'w') as f:
        json.dump(all_stats, f, indent=4)

    return world_series_winner


def postseason_round(teams):
    all_stats = []
    wc_winner1, stats = simulate_series(teams[3], teams[4], 3, "Wild Card", "logs/Wild Card")
    all_stats.append(stats)
    wc_winner2, stats = simulate_series(teams[2], teams[5], 3, "Wild Card", "logs/Wild Card")
    all_stats.append(stats)

    ds_winner1, stats = simulate_series(teams[0], wc_winner1, 5, "Division Series", "logs/Division Series")
    all_stats.append(stats)
    ds_winner2, stats = simulate_series(teams[1], wc_winner2, 5, "Division Series", "logs/Division Series")
    all_stats.append(stats)

    cs_winner, stats = simulate_series(ds_winner1, ds_winner2, 7, "Championship Series", "logs/Championship Series")
    all_stats.append(stats)

    return cs_winner, all_stats
