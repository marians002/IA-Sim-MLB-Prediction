# Regla del Cambio de Pitcher Basado en el Conteo de Lanzamientos y el Bateador Oponente
def change_pitcher_rule(game_state):
    if game_state['pitch_count'] > 100 and game_state['opponent_batter'] == 'left':
        return True
    return False


# Regla del Robo de Base
def steal_base_rule(game_state):
    if game_state['runner_on_first'] and game_state['outs'] < 2 and game_state['pitcher'] == 'right':
        return True
    return False


# Regla del Toque de Bola:
def bunt_rule(game_state):
    if game_state['runner_on_first'] and game_state['outs'] == 0 and game_state['inning'] < 6:
        return True
    return False


# Regla del Desafío del Manager:
def challenge_rule(game_state):
    if game_state['close_play'] and game_state['challenges_left'] > 0:
        return True
    return False


# Regla del Cambio Defensivo
def defensive_shift_rule(game_state):
    if game_state['opponent_batter'] == 'left' and game_state['inning'] > 7 and game_state['score_difference'] <= 2:
        return True
    return False


# Uso del Bullpen: Si el lanzador abridor ha permitido más de 3 carreras en las últimas 2 entradas, considerar
# cambiar al relevista.
def bullpen_usage_rule(game_state):
    if game_state['runs_allowed_last_2_innings'] > 3:
        return True
    return False


# Cambio de Bateador: Si el equipo está perdiendo por 1 carrera en la última entrada y hay un bateador con un
# promedio de bateo bajo, considerar un bateador emergente.
def pinch_hitter_rule(game_state):
    if game_state['inning'] == 9 and game_state['score_difference'] == -1 and game_state['current_batter_avg'] < 0.200:
        return True
    return False


# Estrategia de Bateo y Carrera: Si hay un corredor en primera base y menos de 2 outs, considerar la estrategia de
# bateo y carrera.
def hit_and_run_rule(game_state):
    if game_state['runner_on_first'] and game_state['outs'] < 2:
        return True
    return False


# Defensa en el Infield: Si hay un corredor en tercera base y menos de 2 outs, jugar con la defensa del infield
# adentro para prevenir una carrera
def infield_in_rule(game_state):
    if game_state['runner_on_third'] and game_state['outs'] < 2:
        return True
    return False


# Cambio de Posición Defensiva: Si el bateador contrario tiene una alta tendencia a batear hacia el lado derecho del
# campo, ajustar la defensa hacia ese lado.
def defensive_positioning_rule(game_state):
    if game_state['opponent_batter_tendency'] == 'right':
        return True
    return False
