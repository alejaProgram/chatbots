from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import datetime
import csv

app = Flask(__name__)
CORS(app)

# Configura tu API key
genai.configure(api_key="AIzaSyAeNetDVYBzEzwyxh99mBmTlsiJJQiIvzE")

# Lee el contexto
with open("context.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

# CAMBIO PRINCIPAL: Usar un modelo actualizado
# Opciones disponibles (elige una):
# modelo = genai.GenerativeModel("gemini-1.5-flash")  # Más rápido y económico
modelo = genai.GenerativeModel("gemini-1.5-pro")     # Más potente

# Inicia el chat
chat = modelo.start_chat(history=[])

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        pregunta = data.get("pregunta", "")
        
        if not pregunta:
            return jsonify({"error": "No se proporcionó ninguna pregunta"}), 400
        
        prompt = contexto + f"\nUsuario: {pregunta}\nChatbot:"
        respuesta = chat.send_message(prompt).text
        
        # Registrar en CSV
        with open("registro_chat.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.datetime.now(), pregunta, respuesta])
        
        return jsonify({"respuesta": respuesta})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK", "message": "Servidor funcionando correctamente"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)