from simulator.game_state import *


# Regla del Cambio de Pitcher Basado en el Conteo de Lanzamientos
def change_pitcher_rule(game_state: GameState):
    if game_state.pitch_count > 70:
        return True
    return False


# Regla del Robo de Base
def steal_base_rule(game_state: GameState):
    if game_state.runner_on_first and game_state.outs < 2 and game_state.pitcher.pitch_hand == 'R':
        if game_state.batter.sprint_speed and game_state.batter.sprint_speed > 29:
            return True
    return False


# Regla del Toque de Bola:
# Si hay un corredor en primera base y no hay corredores en segunda o tercera base, no hay outs,
# y el promedio de bateo del bateador es menor a 0.250, considerar el toque de bola.
def bunt_rule(game_state: GameState):
    if (game_state.runner_on_first and not game_state.runner_on_third and not game_state.runner_on_second and
            game_state.outs < 2 and game_state.batter.avg < 0.250):
        return True
    return False


# Regla del Desafío del Manager:
def challenge_rule(game_state: GameState):
    if game_state.close_play and game_state.challenges_left > 0:
        return True
    return False


# Regla del Cambio Defensivo
def defensive_shift_rule(game_state: GameState):
    # if game_state.opponent_batter == 'left' and game_state.inning > 7 and game_state.score_difference <= 2:
    #     return True
    return False


# Uso del Bullpen: Si el lanzador abridor ha permitido más de 3 carreras en las últimas 2 entradas, considerar
# cambiar al relevista.
def bullpen_usage_rule(game_state: GameState):
    if game_state.runs_allowed_last_2_innings > 3:
        return True
    return False


# Cambio de Bateador: Si el equipo está perdiendo por 1 o 2 carreras en la 8va o 9na entrada y hay un bateador con un
# promedio de bateo bajo, considerar un bateador emergente.
def pinch_hitter_rule(game_state: GameState):
    if game_state.inning >= 8 and game_state.batter.avg < 0.200:
        score_difference = game_state.home_score - game_state.away_score
        if game_state.batting_team == 0:  # Batean los visitantes
            return score_difference == 1 or score_difference == 2
        else:  # Batean los locales
            return score_difference == -1 or score_difference == -2


# Estrategia de Corrido y Bateo: Si hay un corredor en primera base y menos de 2 outs, considerar la
# estrategia de corrido y bateo.
def hit_and_run_rule(game_state: GameState):
    if game_state.runner_on_first and game_state.outs < 2 and game_state.batter.avg > 0.200:
        return True
    return False


# Defensa en el Infield: Si hay un corredor en tercera base y menos de 2 outs, jugar con la defensa del infield
# adentro para prevenir una carrera
def infield_in_rule(game_state: GameState):
    if game_state.runner_on_third and game_state.outs < 2:
        return True
    return False


# Cambio de Posición Defensiva: Si el bateador contrario tiene una alta tendencia a batear hacia el lado derecho del
# campo, ajustar la defensa hacia ese lado.
def defensive_positioning_rule(game_state: GameState):
    # if game_state.opponent_batter_tendency == 'right':
    #     return True
    return False
