from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LLAMA_API_KEY = 'LA-ce8287c47a2943b19e9ff328f027d0050b716e1c93e3471fa76a3c5de2bd663f'

@app.route('/generate', methods=['POST'])
def generate_decree():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "Prompt is missing"}), 400

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LLAMA_API_KEY}'
    }
    
    payload = {
        "model": "llama-2-70b-chat",
        "messages": [
            {"role": "system", "content": "Eres un experto en crear decretos positivos y poderosos."},
            {"role": "user", "content": f"Crea un decreto inspirador y poderoso sobre: {prompt}"}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    llama_response = requests.post('https://api.llama-api.com/chat/completions', headers=headers, json=payload)

    if llama_response.status_code != 200:
        return jsonify({"error": "Failed to generate response"}), llama_response.status_code

    llama_data = llama_response.json()
    return jsonify(llama_data)

if __name__ == '__main__':
    app.run(debug=True)