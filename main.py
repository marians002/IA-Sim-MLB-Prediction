from data_loader import data_loader as dl
from simulator.game_simulator import *
from manager.baseball_manager import *
from manager.pitcher_selection import *
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

    # Get pitchers
    rotation_t1, bullpen_t1, rotation_t2, bullpen_t2 = get_rotations_bullpens(t1_pitchers, t2_pitchers)

    h_lineup = get_lineup(t1_pitchers, t1_batters)
    a_lineup = get_lineup(t2_pitchers, t2_batters)

    h_lineup[0] = rotation_t1[0]
    a_lineup[0] = rotation_t2[0]

    game_simulator = GameSimulator(BaseballManager(), t1, t2, t1_batters, t2_batters,
                                   h_lineup, a_lineup, bullpen_t1, bullpen_t2)
    game_simulator.simulate_game()
    game_simulator.save_log('game_log.json')


if __name__ == "__main__":
    main()
