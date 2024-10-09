from data_loader import data_loader as dl
from simulator.game_simulator import *
from manager.baseball_manager import *
from manager.RuleClass import *
from manager.rules_conditions import *
from genetica.mlbeticA import *


def main():
    teams = dl.load_data()

    # Select two random teams:
    # They will be fixed by the moment
    t1 = teams[12]
    t2 = teams[10]
    # dl.print_team_rosters([t1, t2])

    t1_pitchers, t1_batters = dl.separate_pitchers_batters(t1)
    t2_pitchers, t2_batters = dl.separate_pitchers_batters(t2)

    rules = [
        Rule("Change Pitcher", change_pitcher_condition, change_pitcher_action),
        Rule("Steal Base", steal_base_condition, steal_base_action),
        Rule("Bunt", bunt_condition, bunt_action),
        Rule("Pinch Hitter", pinch_hitter_condition, pinch_hitter_action),
        Rule("Hit and Run", hit_and_run_condition, hit_and_run_action),
        Rule("Intentional Walk", intentional_walk_condition, intentional_walk_action),
        Rule("Pickoff", pickoff_condition, pickoff_action)
        # Rule("Infield In", infield_in_condition, infield_in_action),
        # Rule("Defensive Positioning", defensive_positioning_condition, defensive_positioning_action),
        # Rule("Challenge", challenge_condition, challenge_action),
        # Rule("Defensive Shift", defensive_shift_condition, defensive_shift_action),
        # Rule("Bullpen Usage", bullpen_usage_condition, bullpen_usage_action),
    ]

    manager = BaseballManager(rules)

    # t = get_lineup(t1_pitchers, t1_batters)

    # Test lineup (Default batters and pitchers)
    h_lineup = [t1_pitchers[0]]
    t1_pitchers.pop(0)  # Remove the opening pitcher from the bullpen
    a_lineup = [t2_pitchers[0]]
    t2_pitchers.pop(0)  # Remove the opening pitcher from the bullpen

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
