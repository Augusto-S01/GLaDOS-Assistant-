import json
import time
import logging
import os
import base64
from tempfile import NamedTemporaryFile
from flask import Flask, request, jsonify
from transcriber import transcribe_audio
import soundfile as sf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def process_audio(audio_data_base64):
    if not audio_data_base64:
        logger.warning("Audio data (base64) not found in request")
        return jsonify({"error": "Audio data (base64) not found in request"}), 400

    logger.info("Audio data received, decoding base64...")

    try:

        audio_data = base64.b64decode(audio_data_base64)


        temp_audio_file = "temp_audio_received.wav"
        with open(temp_audio_file, "wb") as f:
            f.write(audio_data)


        try:
            with sf.SoundFile(temp_audio_file) as sf_file:
                original_samplerate = sf_file.samplerate
                logger.info(f"Audio format: {sf_file.format}, Samplerate: {sf_file.samplerate}")

  
                if sf_file.channels != 1:
                    logger.warning("Audio has more than 1 channel, converting to mono.")
                    audio_data = sf_file.read(dtype='int16')  
                    sf.write(temp_audio_file, audio_data, original_samplerate)
                else:
                    audio_data = sf_file.read(dtype='int16')
                    sf.write(temp_audio_file, audio_data, original_samplerate)

        except Exception as e:
            logger.error(f"Invalid audio file: {e}")
            return jsonify({"error": f"Invalid audio file: {e}"}), 400

        transcribed_text = transcribe_audio(temp_audio_file)
        logger.info(f"Transcribed text: {transcribed_text}")

        result_message = {
            "content": transcribed_text
        }

        return jsonify(result_message), 200

    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        return jsonify({"error": f"Error processing audio: {e}"}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    audio_data_base64 = data.get("audio_data", "")
    return process_audio(audio_data_base64)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)