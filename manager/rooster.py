import statsapi

# Get roster for a specific team
team_id = 147  # Example: New York Yankees
roster = statsapi.roster(team_id, season=2023)

print(roster)
