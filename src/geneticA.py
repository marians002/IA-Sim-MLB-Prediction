import random
import time
import itertools
import random
import math

def order_one_crossover(parent1, parent2):
    size = len(parent1)
    child1, child2 = [None]*size, [None]*size

    # Step 1: Select crossover points
    cx_point1, cx_point2 = sorted(random.sample(range(size), 2))

    # Step 2: Copy segments
    child1[cx_point1:cx_point2] = parent1[cx_point1:cx_point2]
    child2[cx_point1:cx_point2] = parent2[cx_point1:cx_point2]

    # Step 3: Fill remaining positions
    fill_positions(child1, parent2)
    fill_positions(child2, parent1)

    return child1, child2

def fill_positions(child, parent):
    size = len(parent)
    current_pos = 0
    for elem in parent:
        if elem not in child:
            while child[current_pos] is not None:
                current_pos +=1
            child[current_pos] = elem

def fitness_sort(object):
    """ most valued elemnts goes back """
    val = 0
    mul = 1
    for element in object:
        val += element*mul
        mul+=1
        
    return val

def initial_population(pool, population_size):
    return random.sample(pool, population_size)

def weighted_by(population, fitness):
    """ Returns a probability according to the weights """
    weights = [fitness(p) for p in population]
    total_weight = sum(weights)
    
    return [w/total_weight for w in weights]

def crossover(parent1, parent2):
    c = random.randint(0, len(parent1))
    return parent1[:c] + parent2[c:]

""" def mutate(team, player_pool):
    new_players = team.players[:]
    idx1, idx2 = random.sample(range(len(new_players)), 2)
    new_players[idx1], new_players[idx2] = new_players[idx2], new_players[idx1]
    return Team(new_players) """

def mutate(child, pool):
    if random.random() < 0.05:  
        return child
    return child


def select_parent(population, weights):
    total_fitness = sum(weights)
    pick = random.uniform(0,total_fitness)
    
    current = 0
    for individual, fitness_value in zip(population, weights):
        current += fitness_value
        if current >= pick:
            return individual                   
    
    return population[0]

def genetic_algo(population, fitness):
    start_time = time.time()
    
    max_individual = None
    max_val = -math.inf
    
    while True:
        weigths = weighted_by(population, fitness)
        new_population = []
        
        for i in range(len(population)//2):
            parent1, parent2 =  select_parent(population, weigths), select_parent(population, weigths)
            
            child1, child2 = order_one_crossover(parent1, parent2)
        
            child1 = mutate(child1, pool)
            child2 = mutate(child2, pool)    
            
            new_population.extend([child1, child2])
        
        #elitism, keep the best individuals and punish the worse
        
        population.sort(key=fitness, reverse=True)
        new_population.sort(key=fitness, reverse=False)
        
        if fitness(population[0]) >= fitness(new_population[1]) and fitness(population[1]) >= fitness(new_population[0]):
            population = new_population
        else: 
            population[2:] = new_population [2:]
        
        best = max(population, key=fitness)
        
        if fitness(best) > max_val:
            max_individual = best
        if time.time() - start_time > 20: break
        
    return max_individual

#### PSUDOCODE ####
""" function GENETIC ALGORITHM(population, ﬁtness) returns an individual
        repeat
            weights← WEIGHTED BY(population, ﬁtness)
            population2← empty list
            
            for i = 1 to SIZE( population) do
                parent1, parent2← WEIGHTED RANDOM CHOICES (population, weights, 2)
            
            child ← REPRODUCE (parent1, parent2)
            
            if (small random probability) then child ← MUTATE(child)
                add child to population2
                population← population2
        
        until some individual is ﬁt enough, or enough time has elapsed
        
        return the best individual in population, according to ﬁtness
        
    
    function R EPRODUCE (parent1, parent2) returns an individual
        n ← L ENGTH(parent1)
        c ← random number from 1 to n
        
        return A PPEND(S UBSTRING (parent1, 1, c), SUBSTRING (parent2, c + 1, n)) """
##################
numbers = list(range(1, 11))
permutations = list(itertools.permutations(numbers))

pool = numbers
init_population = initial_population(permutations, 20)

ans = genetic_algo(init_population, fitness_sort)
print(ans)