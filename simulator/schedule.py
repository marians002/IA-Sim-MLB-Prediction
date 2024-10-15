import random, json
from simulator.series_simulator import simulate_series


def generate_schedule(teams: list):
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
