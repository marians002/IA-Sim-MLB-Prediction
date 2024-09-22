from data_loader import data_loader as dl
from simulator.game_simulator import *
from manager.baseball_manager import *
from manager.rules import *
from genetica.mlbeticA import *


def main():
    teams = dl.load_data()

    # Select two random teams:
    # They will be fixed by the moment
    t1 = teams[12]
    t2 = teams[13]
    # dl.print_team_rosters([t1, t2])

    t1_pitchers, t1_batters = dl.separate_pitchers_batters(t1)
    t2_pitchers, t2_batters = dl.separate_pitchers_batters(t2)

    manager = BaseballManager()
    rules = [change_pitcher_rule, steal_base_rule, bunt_rule, challenge_rule, defensive_shift_rule,
             bullpen_usage_rule, pinch_hitter_rule, hit_and_run_rule, intentional_walk_rule, infield_in_rule,
             defensive_positioning_rule]
    for rule in rules:
        manager.add_rule(rule)
    # t = get_lineup(t1_pitchers, t1_batters)

    # Test lineup (Default batters and pitchers)
    h_lineup = [t1_pitchers[0]]
    t1_pitchers.pop(0)    # Remove the opening pitcher from the bullpen
    a_lineup = [t2_pitchers[0]]
    t2_pitchers.pop(0)    # Remove the opening pitcher from the bullpen

    # Posteriormente hay que cambiar las dos lineas de arriba para que se elija un pitcher y ese pitcher se coloque en
    # la posicion 0 del listado de pitchers para hacer cositas con los cambios de pitcher luego

    for i in range(10):
        h_lineup.append(t1_batters[i])
        a_lineup.append(t2_batters[i])

    game_simulator = GameSimulator(manager, t1, t2, t1_batters, t1_pitchers, t2_batters, t2_pitchers, h_lineup, a_lineup)
    game_simulator.simulate_game()
    game_simulator.save_log('game_log.json')


if __name__ == "__main__":
    main()

# Genetic algorithm example
# pool = players
# init_population = []
# for i in range(20):
#     init_population.append(random.sample(players, 9))
# fitness = fitness_lineup
# ans = geneticA.genetic_algo(population=init_population, fitness=fitness, pool=pool)

# Case of use
# Fitness function is max when numeric array is ordered
# numbers = list(range(1, 11))
# permutations = list(itertools.permutations(numbers))
# parents = random.sample(permutations, 2)
# child1, child2 = geneticA.order_one_crossover(parents[0], parents[1])
# pool = numbers
# init_population = random.sample(permutations, 20)
# ans = geneticA.genetic_algo(init_population, geneticA.fitness_sort, pool)
# print(ans)
