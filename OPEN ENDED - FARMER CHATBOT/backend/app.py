import os
import speech_recognition as sr
from flask import Flask, request, jsonify, render_template, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
dhenu_api_key = os.getenv("DHENU_API_KEY")
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

print("Loaded DHENU API Key:", dhenu_api_key)
print("Loaded OpenWeather API Key:", weather_api_key)

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

# Setup Dhenu-compatible OpenAI client
client = OpenAI(
    base_url="https://api.dhenu.ai/v1",
    api_key=dhenu_api_key
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response = client.chat.completions.create(
            model="dhenu2-in-8b-preview",
            messages=[{"role": "user", "content": user_message}]
        )
        
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather', methods=['GET'])
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude parameters are required."}), 400

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
    
    try:
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        return jsonify(weather_response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch weather data", "details": str(e)}), 500

@app.route('/voice', methods=['GET'])
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return jsonify({'success': True, 'text': text})

        except sr.UnknownValueError:
            return jsonify({'success': False, 'error': 'Could not understand the speech'}), 400
        except sr.RequestError:
            return jsonify({'success': False, 'error': 'Could not process the request'}), 500

# Serve static files properly
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
