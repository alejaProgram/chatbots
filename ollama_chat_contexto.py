import requests
import json

def cargar_contexto():

    try:
        with open("context.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("⚠️ Archivo 'context.txt' no encontrado. Usando contexto vacío.\n")
        return ""

def chat_with_ollama(model="llama3.1:latest"):
    print("🤖 Chat con Ollama (escribe 'salir' para terminar)\n")
    context = cargar_contexto()
    while True:
        user_input = input("Tú: ")

        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("🛑 Chat finalizado.")
            break

        data = {
            "model": model,
            "prompt": f"actue como chatbot, tenga en cuenta esta información {context} "+" y responda : "+user_input,
            "stream": False
        }

        try:
            # Petición sin stream, respuesta completa
            print("...Pensando...")
            response = requests.post("http://localhost:11434/api/generate", json=data)
            response.raise_for_status()
            result = response.json()

            print(">", result["response"], "\n")

        except Exception as e:
            print(f"❌ Error al comunicarse con Ollama: {e}\n")

# Ejecutar chat
chat_with_ollama()
