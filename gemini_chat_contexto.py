import requests
import json


def cargar_contexto():
    try:
        with open("context.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("⚠️ Archivo 'context.txt' no encontrado. Usando contexto vacío.\n")
        return ""


def chat_with_gemini(api_key, model="gemini-1.5-flash"):
    print("🤖 Chat con Gemini (escribe 'salir' para terminar)\n")
    context = cargar_contexto()

    # URL de la API de Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    

    while True:
        user_input = input("Tú: ")

        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("🛑 Chat finalizado.")
            break

        # Formato de datos para Gemini API
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Actúa como chatbot, ten en cuenta esta información: {context}\n\nY responde: {user_input}"
                        }
                    ]
                }
            ]
        }

        try:
            print("...Pensando...")
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()

            # Extraer la respuesta de Gemini
            if "candidates" in result and len(result["candidates"]) > 0:
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                print(">", content, "\n")
            else:
                print("❌ No se pudo obtener respuesta de Gemini\n")

        except Exception as e:
            print(f"❌ Error al comunicarse con Gemini: {e}\n")


# Configuración
API_KEY = ""  # Reemplaza con tu API key de Google

# Ejecutar chat
if __name__ == "__main__":
    if API_KEY == "TU_API_KEY_AQUI":
        print("⚠️ Por favor, configura tu API key de Google en la variable API_KEY")
    else:
        chat_with_gemini(API_KEY)