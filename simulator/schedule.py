import random
from collections import defaultdict
from simulator.series_simulator import simulate_series


def generate_schedule(teams : list):
    num_teams = len(teams)
    schedule = []

    # Round-robin algorithm to generate matchups
    for round in range(num_teams - 1):
        for i in range(num_teams // 2):
            home = teams[i]
            away = teams[num_teams - 1 - i]
            schedule.append((home, away))
        teams.insert(1, teams.pop())  # Rotate teams

    # Repeat the schedule to ensure each team plays 162 games
    full_schedule = schedule * (162 // (num_teams - 1))

    # Shuffle the schedule to distribute home and away games
    random.shuffle(full_schedule)

    return full_schedule


def create_postseason_structure(nl_teams, al_teams):
    nl_champion = postseason_round(nl_teams, "NL")
    al_champion = postseason_round(al_teams, "AL")
    
    world_series_winner = simulate_series(nl_champion, al_champion, 7, "World Series", "logs/World Series")
    
    return world_series_winner


def postseason_round(teams, league):
    wc_winner1 = simulate_series(teams[3], teams[4], 3, "Wild Card", "logs/Wild Card")
    wc_winner2 = simulate_series(teams[2], teams[5], 3, "Wild Card", "logs/Wild Card")
    
    ds_winner1 = simulate_series(teams[0], wc_winner1, 5, "Division Series", "logs/Division Series")
    ds_winner2 = simulate_series(teams[1], wc_winner2, 5, "Division Series", "logs/Division Series")
    
    cs_winner = simulate_series(ds_winner1, ds_winner2, 7, "Championship Series", "logs/Championship Series")
    
    return cs_winner

