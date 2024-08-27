import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Configura la clave API de Google en la variable de entorno
os.environ["GOOGLE_API_KEY"] = "AIzaSyAtG48JDc-lIyx8gmjFkIFUbWcVir8LuK8"

def main():
    # Configura el modelo de Google Generative AI usando el nombre correcto del modelo
    model_name = "gemini-1.5-flash"  # Modelo correcto
    model = ChatGoogleGenerativeAI(
        model=model_name)

    while True:
        # Solicita al usuario que introduzca un prompt
        prompt = input("Introduce tu prompt (o escribe 'salir' para terminar): ")

        # Verifica si el usuario quiere salir del ciclo
        if prompt.lower() == 'salir':
            print("Saliendo del programa.")
            break

        # Crea un mensaje con el contenido del prompt
        message = HumanMessage(content=prompt)

        try:
            # Genera la respuesta del modelo usando `invoke`
            response = model.invoke([message])
            
            # Muestra la respuesta al usuario
            print("Respuesta del modelo:")
            print(response.content)

        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
