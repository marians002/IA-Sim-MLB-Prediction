import json
import random
from simulator.series_simulator import simulate_series


def generate_schedule(teams: list, verbose=False):
    """
    Generate a round-robin schedule for the given teams.

    Parameters:
    -----------
    teams : list
        A list of team objects.
    verbose : bool, optional
        If True, prints the generated schedule (default is False).

    Returns:
    --------
    list
        A list of tuples representing the schedule, where each tuple contains two teams.
    """
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

    if verbose:
        print("\033[91m Generated schedule:\033[0m")
        for game in full_schedule:
            print(game[0].team_name, " vs. ", game[1].team_name)

    print("\033[92mSchedule generated successfully.\033[0m")
    print()
    return full_schedule


def create_postseason_structure(nl_teams, al_teams):
    """
    Create the postseason structure and simulate the series.

    Parameters:
    -----------
    nl_teams : list
        A list of National League team objects.
    al_teams : list
        A list of American League team objects.

    Returns:
    --------
    object
        The team object representing the World Series winner.
    """
    all_stats = []
    nl_champion, stats = postseason_round(nl_teams)
    all_stats.append(stats)
    al_champion, stats = postseason_round(al_teams)
    all_stats.append(stats)

    world_series_winner, stats = simulate_series(nl_champion, al_champion, 7)
    all_stats.append(stats)

    # Save all game statistics to a JSON file
    with open('postseason.json', 'w') as f:
        json.dump(all_stats, f, indent=4)

    return world_series_winner


def postseason_round(teams):
    """
    Simulate a postseason round and return the champion.

    Parameters:
    -----------
    teams : list
        A list of team objects participating in the postseason round.

    Returns:
    --------
    tuple
        A tuple containing the champion team object and a list of statistics for each series.
    """
    all_stats = []
    wc_winner1, stats = simulate_series(teams[3], teams[4], 3)
    all_stats.append(stats)
    wc_winner2, stats = simulate_series(teams[2], teams[5], 3)
    all_stats.append(stats)

    ds_winner1, stats = simulate_series(teams[0], wc_winner1, 5)
    all_stats.append(stats)
    ds_winner2, stats = simulate_series(teams[1], wc_winner2, 5)
    all_stats.append(stats)

    cs_winner, stats = simulate_series(ds_winner1, ds_winner2, 7)
    all_stats.append(stats)

    return cs_winner, all_stats