import json
import logging
import os
import base64
from flask import Flask, request, jsonify
from engine import glados_tts
import soundfile as sf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    text = data.get("content", "")

    if not text:
        return jsonify({"error": "Content not found in the request"}), 400

    logger.info(f"Text to synthesize: {text}")

    glados_tts(text)

    audio_file_path = 'audio/GLaDOS-tts-temp-output.wav'
    if not os.path.exists(audio_file_path):
        logger.error(f"Audio file not found: {audio_file_path}")
        return jsonify({"error": f"Audio file not found: {audio_file_path}"}), 500

    try:
        with open(audio_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')  

            with sf.SoundFile(audio_file_path) as f:
                samplerate = f.samplerate
                logger.info(f"Sample rate of the audio file: {samplerate} Hz")

            result_message = {
                "audio_data": audio_base64,
                "samplerate": samplerate  
            }

            return jsonify(result_message), 200

    except Exception as e:
        logger.error(f"Error reading audio file: {e}")
        return jsonify({"error": f"Error reading audio file: {e}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
