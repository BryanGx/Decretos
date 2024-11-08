from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa la extensión de CORS para manejar solicitudes de origen cruzado
import requests
import os

# Configuración de la aplicación Flask y CORS
app = Flask(__name__)

CORS(app, resources={r"/generate": {"origins": "http://decretos.42web.io"}})
# Obtén tu API Key desde una variable de entorno para mayor seguridad
LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')  # Asegúrate de que esta variable esté configurada en tu entorno

@app.route('/generate', methods=['POST'])
def generate_decree():
    # Recibe y valida los datos de la solicitud
    data = request.json
    prompt = data.get('prompt', '')

    # Verifica que el campo 'prompt' no esté vacío
    if not prompt:
        return jsonify({"error": "Prompt is missing"}), 400

    # Define los encabezados de la solicitud, incluyendo la API Key de autenticación
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LLAMA_API_KEY}'
    }
    
    # Configura el payload para la API con el modelo, los mensajes, y los parámetros de generación
    payload = {
        "model": "llama-2-70b-chat",
        "messages": [
            {"role": "system", "content": "Eres un experto en crear decretos positivos y poderosos."},
            {"role": "user", "content": f"Crea un decreto inspirador y poderoso sobre: {prompt}"}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    # Realiza la solicitud a la API de Llama para obtener el decreto
    try:
        llama_response = requests.post('https://api.llama-api.com/chat/completions', headers=headers, json=payload)
        llama_response.raise_for_status()  # Verifica si la solicitud fue exitosa
    except requests.exceptions.RequestException as e:
        # Maneja errores de conexión o de respuesta de la API
        return jsonify({"error": "Failed to generate response", "details": str(e)}), 500

    # Extrae los datos de la respuesta de la API y envíalos como JSON
    llama_data = llama_response.json()
    return jsonify(llama_data)

# Inicia el servidor
if __name__ == '__main__':
    # Define el puerto de la aplicación desde variables de entorno, con valor predeterminado 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
