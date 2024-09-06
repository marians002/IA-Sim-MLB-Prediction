import pandas as pd
import geneticA
from MLBpopulation import *
import csv
import os
import itertools
import statsapi

""" # Get roster for a specific team
team_id = 147  # Example: New York Yankees
roster = statsapi.roster(team_id, season=2023)

print(roster) """

# Get the path to the CSV file
current_dir = os.path.dirname(__file__)

csv_path = os.path.join(current_dir, 'datasets', 'pitchers.csv')
# Read the CSV file into a DataFrame
pitchers = pd.read_csv(csv_path)

csv_path = os.path.join(current_dir, 'datasets', 'batters.csv')
# Read the CSV file into a DataFrame
batters = pd.read_csv(csv_path)

# Display the DataFrame
print(batters.columns)
print(pitchers.columns)
print(batters.values[0])
myPlayer = Batter(list(batters.values[0]))    

players = []
for _, row in batters.iterrows():
    players.append(Batter(list(row)))
    
    
print(players[24])

#teams = get_teams(batters, pitchers)

""" 
Dont know why this test dont work. Geet stick in a cycle...
pool = players

init_population = []
for i in range(20):
    init_population.append(random.sample(players, 9))

fitness = fitness_lineup
ans = geneticA.genetic_algo(population=init_population, fitness=fitness, pool=pool)
 """
# case of use
# Fitness func is max when numeric array is ordered
numbers = list(range(1, 11))
permutations = list(itertools.permutations(numbers))

pool = numbers
init_population = geneticA.initial_population(permutations, 20)

ans = geneticA.genetic_algo(init_population, geneticA.fitness_sort, pool)

print(ans)



