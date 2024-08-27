from pybaseball import statcast_batter

# Get data for a specific player
data = statcast_batter(start_dt='2023-01-01', end_dt='2023-12-31', player_id=660271)

# Analyze the direction of batted balls
pull_hits = data[data['hc_x'] < 125]  # Example condition for pull hits
center_hits = data[(data['hc_x'] >= 125) & (data['hc_x'] <= 175)]  # Example condition for center hits
oppo_hits = data[data['hc_x'] > 175]  # Example condition for opposite field hits

# Calculate percentages
pull_percentage = len(pull_hits) / len(data) * 100
center_percentage = len(center_hits) / len(data) * 100
oppo_percentage = len(oppo_hits) / len(data) * 100

tendency = "center"

# Find the highest percentage
if pull_percentage > center_percentage:
    if pull_percentage > oppo_percentage:
        tendency = "left"
    else:
        tendency = "right"
elif oppo_percentage > center_percentage:
    tendency = "right"

# Print the highest percentage
print("Highest Tendency: ", tendency)
