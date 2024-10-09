from gtts import gTTS
import pygame
import io
from chat import *

file_path = 'game_log.json'
team1 = 'Orioles'
team2 = 'Yankees'
prompt = generate_prompt_from_game_log(file_path, team1, team2)

ans = get_gemini_response(prompt)
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
