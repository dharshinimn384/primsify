from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors module
import os
import json
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in your Flask app

# Set your PaLM API Key
os.environ['PALM_API_KEY'] = "AIzaSyAqL5QXqg1pjVOSNkD58FDtRlfQTZMLALM"

def generate_text(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={os.getenv('PALM_API_KEY')}"
    headers = {'Content-Type': 'application/json'}
    data = {"prompt": {"text": prompt}}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        generated_text = response.json()
        return generated_text
    else:
        return f"Failed to generate text. Status code: {response.status_code}"

@app.route('/generate-text', methods=['POST'])
def generate_text_route():
    try:
        data = request.json
        user_prompt = data['prompt']
        result = generate_text(user_prompt)
        if 'candidates' in result and len(result['candidates']) > 0:
            generated_output = result['candidates'][0]['output']
            return jsonify({"AI": generated_output})
        else:
            return jsonify({"AI": "Unable to generate a response."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
