from gtts import gTTS
import pygame
import io
from chat import get_gemini_response
prompt = """ explicacion del contexto: 

    pitch_count: Número de lanzamientos realizados por el pitcher hasta el momento en el juego o inning.

    action: Indica si el manager tomó una decisión o no. "No action" significa que no dio instrucciones específicas.

    result: Resultado de la jugada más reciente, como un out, hit o base por bolas.

    game_state: Estado actual del juego, incluye información sobre inning, corredores, outs y más.

        opponent_batter: Número del turno del bateador del equipo contrario o el que está actualmente bateando.

        runner_on_first: Indica si hay un corredor en la primera base.

        runner_on_second: Indica si hay un corredor en la segunda base.

        runner_on_third: Indica si hay un corredor en la tercera base.

        outs: Cantidad de outs (eliminaciones) en el inning actual.

        inning: Número del inning en curso en el partido.

        close_play: Indica si hubo una jugada ajustada o controvertida.

        challenges_left: Oportunidades restantes para desafiar decisiones arbitrales.

        pitcher_hand: Mano dominante del lanzador (diestro o zurdo).

        score_difference: Diferencia de puntuación entre los equipos.

        runs_allowed_last_2_innings: Carreras permitidas en los últimos dos innings por el equipo defensor.

        current_batter_avg: Promedio de bateo del bateador actual.

        opponent_batter_tendency: Tendencia del bateador contrario, a la derecha del campo o a la izquierda de campo.

        home_score: Número de carreras anotadas por el equipo local.

        away_score: Número de carreras anotadas por el equipo visitante.


    contexto de la jugada: {
        "pitch_count": 1,
        "action": "No action",
        "result": "out",
        "game_state": {
            "pitch_count": 1,
            "opponent_batter": 1,
            "runner_on_first": false,
            "runner_on_second": false,
            "runner_on_third": false,
            "outs": 0,
            "inning": 1,
            "close_play": false,
            "challenges_left": 2,
            "pitcher_hand": "L",
            "score_difference": 0,
            "runs_allowed_last_2_innings": 0,
            "current_batter_avg": 0.207,
            "opponent_batter_tendency": "right",
            "home_score": 0,
            "away_score": 0
        }
        Peticion: Necesito que tu siendo un comentarista deportivo con experiencia 
        me narres esta jugada de forma equilibrada pero tambien emocionante ignora el parametro action, inventa
        la forma en la que se produce el resultado, siempre que tenga sentido en el contexto del beisbol
        
        """
ans = get_gemini_response(prompt)
ans2 = get_gemini_response("""corrige los errores correspondientes al ambito del beisbol como jugadas invalidas
en el partido de la siguiente respuesta: 
"""+ans + "devuevleme solo la respuesta corregida")
# Crear un objeto gTTS
tts = gTTS(ans, lang="es")
# Guardar el objeto de audio en un buffer en memoria
audio_buffer = io.BytesIO()
tts.write_to_fp(audio_buffer)

# Mover el puntero al inicio del buffer
audio_buffer.seek(0)

# Inicializar pygame mixer
pygame.mixer.init()

# Cargar el archivo mp3 desde el buffer
pygame.mixer.music.load(audio_buffer)

# Reproducir el audio
pygame.mixer.music.play()

# Esperar hasta que termine la reproducción
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
