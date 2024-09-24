from gtts import gTTS
import io
from pnl.chat import *

def save_text_to_file(text, file_name):
    """
    Guarda el texto generado en un archivo .txt.

    :param text: El texto a guardar.
    :param file_name: El nombre del archivo de texto.
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Texto guardado en {file_name}")

def save_audio_to_file(text, file_name):
    """
    Genera un archivo de audio a partir del texto y lo guarda en un archivo .mp3.

    :param text: El texto a convertir en audio.
    :param file_name: El nombre del archivo de audio.
    """
    tts = gTTS(text, lang="es")
    tts.save(file_name)
    print(f"Audio guardado en {file_name}")

def generate_text_and_audio(file_path, team1, team2, text_file='game_text.txt', audio_file='game_audio.mp3'):
    """
    Genera el texto y el audio a partir del log del juego, los guarda en archivos,
    pero no reproduce el audio.

    :param file_path: Ruta al archivo de registro del juego (game log).
    :param team1: Nombre del equipo 1.
    :param team2: Nombre del equipo 2.
    :param text_file: Nombre del archivo donde se guardará el texto generado.
    :param audio_file: Nombre del archivo donde se guardará el audio generado.
    :return: El texto generado por el chatbot.
    """
    # Genera el prompt a partir del log del juego y los equipos
    prompt = generate_prompt_from_game_log(file_path, team1, team2)

    # Obtiene la respuesta utilizando la API de chat
    ans = get_gemini_response(prompt)

    # Eliminar todos los asteriscos (*) y almohadillas (#) del texto
    ans = ans.replace("*", "").replace("#", "")

    # Guardar el texto en un archivo
    save_text_to_file(ans, text_file)

    # Guardar el audio en un archivo
    save_audio_to_file(ans, audio_file)

    return ans  # Devolver el texto generado para otras posibles operaciones

def play_audio(audio_file='game_audio.mp3'):
    """
    Reproduce un archivo de audio .mp3.

    :param audio_file: El nombre del archivo de audio a reproducir.
    """
    import pygame

    # Inicializar pygame mixer
    pygame.mixer.init()

    # Cargar y reproducir el archivo mp3
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Esperar hasta que termine la reproducción
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

# Si se ejecuta este archivo directamente
if __name__ == "__main__":
    file_path = 'game_log.json'
    team1 = 'Orioles'
    team2 = 'Yankees'

    # Llamada para generar y guardar el texto y el audio
    generate_text_and_audio(file_path, team1, team2)

    # Si deseas reproducir el audio posteriormente, puedes hacerlo
    play_audio('game_audio.mp3')
