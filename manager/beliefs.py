import random
from simulator.game_state import *


# Regla del Cambio de Pitcher Basado en el Conteo de Lanzamientos
def change_pitcher_condition(game_state: GameState):
    if game_state.home_team_batting:
        if game_state.pitch_count_away >= 70:
            return True
    elif game_state.pitch_count_home >= 70:
        return True
    return False


# Regla del Robo de Base
def steal_base_condition(game_state: GameState):
    if game_state.runner_on_first and game_state.outs < 2 and game_state.pitcher.pitch_hand == 'R':
        if game_state.runner_on_first.sprint_speed and game_state.runner_on_first.sprint_speed > 29:
            return True
    return False


# Regla del Toque de Bola:
# Si hay un corredor en primera base y no hay corredores en segunda o tercera base, no hay outs,
# y el promedio de bateo del bateador es menor a 0.250, considerar el toque de bola.
def bunt_condition(game_state: GameState):
    if (game_state.runner_on_first and not game_state.runner_on_third and not game_state.runner_on_second and
            game_state.outs < 2 and game_state.batter.avg < 0.250):
        return True
    return False


# Cambio de Bateador: Si el equipo está perdiendo por 1 o 2 carreras en la 8va o 9na entrada y hay un bateador con un
# promedio de bateo bajo, considerar un bateador emergente.
def pinch_hitter_condition(game_state: GameState):
    if game_state.inning >= 8 and game_state.batter.avg < 0.200:
        score_difference = game_state.home_score - game_state.away_score
        if game_state.home_team_batting:
            return score_difference == -1 or score_difference == -2
        else:
            return score_difference == 1 or score_difference == 2


# Estrategia de Corrido y Bateo: Si hay un corredor rápido en primera base y menos de 2 outs, considerar la
# estrategia de corrido y bateo.
def hit_and_run_condition(game_state: GameState):
    if (
            game_state.runner_on_first and game_state.runner_on_first.sprint_speed and game_state.runner_on_first.sprint_speed > 28
            and game_state.outs < 2 and game_state.batter.avg > 0.260):
        return True
    return False


# Intentional Walk Rule: Si hay corredores en segunda y tercera base, primera está libre y
# menos de 2 outs, considerar dar un pase intencional
def intentional_walk_condition(game_state: GameState):
    if (game_state.runner_on_third and game_state.runner_on_second and not game_state.runner_on_first
            and game_state.outs < 2 and game_state.batter.avg > 0.280):
        return True
    return False


# Defensa en el Infield: Si hay corredor en primera base y menos de 2 outs, considerar la defensa en el infield.
def infield_in_condition(game_state: GameState):
    return game_state.runner_on_first and game_state.outs < 2


# Regla de tirar a primera base o tercera base según si el pitcher es zurdo o derecho.
def pickoff_condition(game_state: GameState):
    if (game_state.pitcher.pitch_hand == 'L'
            and game_state.runner_on_first and game_state.runner_on_first.sprint_speed > 27):
        # Se vira a primera con probabilidad del 0.2
        return random.random() < 0.2
    elif (game_state.pitcher.pitch_hand == 'R'
          and game_state.runner_on_third and game_state.runner_on_third.sprint_speed > 27):
        # Se vira a tercera con probabilidad del 0.1
        return random.random() < 0.1
