import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Configura la clave API de Google en la variable de entorno
os.environ["GOOGLE_API_KEY"] = "AIzaSyAtG48JDc-lIyx8gmjFkIFUbWcVir8LuK8"

# Configura el modelo de Google Generative AI usando el nombre correcto del modelo
model_name = "gemini-1.5-flash"  # Modelo correcto
model = ChatGoogleGenerativeAI(model=model_name)

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
    prompt = input("Introduce tu prompt: ")

    # Obtén la respuesta del modelo
    respuesta = get_gemini_response(prompt)

    # Muestra la respuesta al usuario
    print("Respuesta del modelo:")
    print(respuesta)
