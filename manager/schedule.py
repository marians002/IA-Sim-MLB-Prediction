import random
from collections import defaultdict


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

def determine_postseason_teams(divisions, standings):
    # Determine division winners
    division_winners = []
    wild_cards = []
    
    for division in divisions:
        division_standings = sorted(division, key=lambda x: standings[x], reverse=True)
        division_winners.append(division_standings[0])
        wild_cards.extend(division_standings[1:])
    
    # Determine wild card teams
    wild_cards = sorted(wild_cards, key=lambda x: standings[x], reverse=True)[:2]
    
    return division_winners, wild_cards

# def determine_postseason_structure(division_winners):
#     """Determine the postseason structure based on MLB rules."""
#     # Sort teams by standings
#     sf_winner1 = None
#     sf_winner2 = None
#     for division in division_winners:
#         # Wild Card Round
#         wc_winner1 = simulate_series(sorted_teams[2], sorted_teams[5], 3)
#         wc_winner2 = simulate_series(sorted_teams[3], sorted_teams[4], 3)
        
#         # Division Series
#         ds_winner1 = simulate_series(sorted_teams[0], wc_winner2, 3)
#         ds_winner2 = simulate_series(sorted_teams[1], wc_winner1, 3)
        
#         # Semifinals
#         sf_winner1 = simulate_series(ds_winner1, ds_winner2, 3)
        
#         # Final
#     final_winner = simulate_series(sf_winner1, sf_winner1, 7)
    
#     return final_winner

