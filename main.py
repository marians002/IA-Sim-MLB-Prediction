from data_loader import data_loader as dl
from simulator.game_simulator import *
from manager.baseball_manager import *
from genetica.mlbeticA import *
from manager.schedule import *

import json

def save_final_statistics(schedule, filename='final_statistics.json'):
    all_game_stats = []

    for game in schedule:
        t1, t2 = game
        t1_pitchers, t1_batters = dl.separate_pitchers_batters(t1)
        t2_pitchers, t2_batters = dl.separate_pitchers_batters(t2)

        manager_t1 = BaseballManager()
        manager_t2 = BaseballManager()

        h_lineup = [t1_pitchers[0]]
        t1_pitchers.pop(0)  # Remove the opening pitcher from the bullpen
        a_lineup = [t2_pitchers[0]]
        t2_pitchers.pop(0)  # Remove the opening pitcher from the bullpen

        for i in range(10):
            h_lineup.append(t1_batters[i])
            a_lineup.append(t2_batters[i])

        game_simulator = GameSimulator(manager_t1, manager_t2, t1, t2, t1_batters, t1_pitchers, t2_batters, t2_pitchers,
                                       h_lineup, a_lineup)
        game_simulator.simulate_game()
        game_simulator.save_log()
        
        # Collect final statistics
        game_stats = game_simulator.get_final_statistics()
        all_game_stats.append(game_stats)

    # Save all game statistics to a JSON file
    with open(filename, 'w') as f:
        json.dump(all_game_stats, f, indent=4)


def main():
    teams = dl.load_data()
    
    schedule = generate_schedule(teams)
    save_final_statistics(schedule)
    
    


if __name__ == "__main__":
    main()