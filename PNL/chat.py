import os
import json
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Configura la clave API de Google en la variable de entorno
os.environ["GOOGLE_API_KEY"] = "AIzaSyAtG48JDc-lIyx8gmjFkIFUbWcVir8LuK8"

# Configura el modelo de Google Generative AI usando el nombre correcto del modelo
model_name = "gemini-1.5-flash"  # Modelo correcto
model = ChatGoogleGenerativeAI(model=model_name)


def generate_prompt_from_game_log(file_path):
    """
    Generates a prompt for the baseball game between two teams using the game log.

    :param file_path: Path to the game log JSON file.
    :param team1: Name of the first team.
    :param team2: Name of the second team.
    :return: Generated prompt string.
    """
    try:
        with open(file_path, 'r') as file:
            game_log = json.load(file)

        prompt = f"Generate the comments for the following baseball game:\n\n"
        prompt += json.dumps(game_log, indent=4)

        return prompt
    except Exception as e:
        return f"Error: {str(e)}"


def get_gemini_response(prompt):
    """
    Esta función toma un prompt como entrada, lo envía al modelo de Google Generative AI,
    y devuelve la respuesta generada.
    
    :param prompt: La consulta que deseas hacerle al modelo.
    :return: La respuesta generada por el modelo.
    """
    # Crea un mensaje con el contenido del prompt
    message = HumanMessage(content=prompt)

    try:
        # Genera la respuesta del modelo usando `invoke`
        response = model.invoke([message])
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"


# Ejemplo de uso en este mismo script
if __name__ == "__main__":
    # Solicita al usuario que introduzca un prompt
    file_path = '../game_log.json'
    prompt = generate_prompt_from_game_log(file_path)

    # Obtén la respuesta del modelo
    respuesta = get_gemini_response(prompt)

    # Muestra la respuesta al usuario
    print("Respuesta del modelo:")
    print(respuesta)
    # Guardar respuesta como archivo md
    with open('Commentary.md', 'w') as file:
        file.write(respuesta)
    with open('Commentary.txt', 'w') as file:
        file.write(respuesta)
