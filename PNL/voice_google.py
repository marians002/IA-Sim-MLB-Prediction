from gtts import gTTS
import pygame
import io


def run_voice():
    # Read commentary.txt
    with open('Commentary.txt', 'r') as file:
        ans = file.read()
    # Crear un objeto gTTS
    tts = gTTS(ans, lang="en-us")

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
        pygame.time.Clock().tick(5)
