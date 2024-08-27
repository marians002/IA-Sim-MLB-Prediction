import pandas as pd
import geneticA
import MLBpopulation
import csv
import os
import itertools

# Get the path to the CSV file
current_dir = os.path.dirname(__file__)

csv_path = os.path.join(current_dir, 'datasets', 'pitchers.csv')
# Read the CSV file into a DataFrame
pitchers = pd.read_csv(csv_path)

batters = os.path.join(current_dir, 'datasets', 'batters.csv')
# Read the CSV file into a DataFrame
batters = pd.read_csv(csv_path)

# Display the DataFrame
print(batters.columns)
print(pitchers.columns)

# case of use
""" numbers = list(range(1, 11))
permutations = list(itertools.permutations(numbers))

pool = numbers
init_population = geneticA.initial_population(permutations, 20)

ans = geneticA.genetic_algo(init_population, geneticA.fitness_sort, pool)
print(ans) """