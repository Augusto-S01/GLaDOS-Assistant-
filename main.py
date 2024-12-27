import sounddevice as sd
import numpy as np
import base64
import json
import threading
import soundfile as sf
import time
import requests
import logging
import sys


SAMPLERATE = 44100 
BLOCKSIZE = 2048    
SILENCE_THRESHOLD = 500 
SILENCE_TIMEOUT = 2 
STT_URL = "http://localhost:5001/transcribe"  
THINKING_URL = "http://localhost:5002/continue_conversation"  
TTS_URL = "http://localhost:5003/tts"  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


conversation_active = True
audio_data = []  
last_audio_time = time.time() 
silence_time = 0 
response_event = threading.Event()  
response_audio = None 


conversation_id = None
access_token = None
conversation_history = []

def audio_callback(indata, frames, time_info, status):
    global last_audio_time, silence_time, audio_data

    if status:
        logger.warning(f"Status: {status}")


    audio_chunk = indata.copy()
    audio_data.append(audio_chunk)


    volume_norm = np.linalg.norm(audio_chunk) * 10

    if volume_norm > SILENCE_THRESHOLD:

        last_audio_time = time.time()
        silence_time = 0
    else:
      
        silence_time += frames / SAMPLERATE

    
    sys.stdout.write(f"\rAccumulated silence: {silence_time:.2f} seconds")
    sys.stdout.flush()

 
    if silence_time > SILENCE_TIMEOUT:
        logger.info("\nSilence detected. Sending audio to the STT service...")
        send_audio_to_stt()
        silence_time = 0  

def send_audio_to_stt():
    global audio_data, response_audio

    if not audio_data:
        return


    audio_combined = np.concatenate(audio_data, axis=0)


    temp_audio_file = "temp_audio.wav"
    with sf.SoundFile(temp_audio_file, 'w', SAMPLERATE, 1) as f:
        f.write(audio_combined)


    with open(temp_audio_file, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    # Cria a mensagem
    message = {
        "audio_data": audio_base64,
        "samplerate": SAMPLERATE
    }

    logger.info(f"Sending audio to the STT service...")

    try:
        response = requests.post(STT_URL, json=message)
        response.raise_for_status()
        response_data = response.json()
        logger.info("Audio successfully sent to the STT service. Waiting for response...")

        text = response_data.get("content")
        if not text:
            logger.error("Invalid response from STT: text missing.")
            return
        
        logger.info(f"Transcribed text: {text}")

  
        send_text_to_thinking(text)

    except requests.RequestException as e:
        logger.error(f"Error sending audio to the STT: {e}")

    audio_data.clear()

def send_text_to_thinking(text):
    global conversation_id, access_token, conversation_history

    conversation_history.append({"role": "user", "content": text})

    message = {
        "conversation_id": conversation_id,
        "messages": conversation_history,
        "access_token": access_token
    }

    logger.info(f"Sending text to the Thinking service...")

    try:
        response = requests.post(THINKING_URL, json=message)
        response.raise_for_status()
        response_data = response.json()
        logger.info("Text successfully sent to the Thinking service. Waiting for response...")

        assistant_message = response_data.get("assistant_message")
        if not assistant_message:
            logger.error("Invalid response from the Thinking service: assistant message missing.")
            return
        
        logger.info(f"Assistant's message: {assistant_message['content']}")

        conversation_history.append(assistant_message)

        
        send_text_to_tts(assistant_message["content"])

    except requests.RequestException as e:
        logger.error(f"Error sending text to the Thinking service: {e}")


def send_text_to_tts(text):
    message = {
        "content": text
    }

    logger.info(f"Sending text to the TTS service...")


    try:
        response = requests.post(TTS_URL, json=message)
        response.raise_for_status()
        response_data = response.json()
        logger.info("Text successfully sent to the TTS service. Waiting for response...")


        audio_base64 = response_data.get("audio_data")
        samplerate = response_data.get("samplerate", SAMPLERATE)

        if not audio_base64:
            logger.error("Invalid response from the TTS service: audio missing.")
            return

        audio_bytes = base64.b64decode(audio_base64)
        response_audio = np.frombuffer(audio_bytes, dtype=np.int16)

        logger.info(f"Decoded audio size: {len(response_audio)}")
        logger.info(f"Expected samplerate: {samplerate}")


        output_audio_file = "output.wav"
        with sf.SoundFile(output_audio_file, 'w', samplerate, 1) as f:
            f.write(response_audio)
        logger.info(f"Audio saved as {output_audio_file}")


    
        response_event.set()

      
        play_audio(response_audio, samplerate)

    except requests.RequestException as e:
        logger.error(f"Error sending text to the TTS service: {e}")

def play_audio(audio_data, samplerate):
    if audio_data is not None:
        logger.info("Playing received audio...")
        sd.play(audio_data, samplerate=samplerate)
        sd.wait()  
        logger.info("Audio finished. Waiting 2 seconds before recording again.")
        time.sleep(2) 

def main():
    global conversation_active, conversation_id, access_token, conversation_history


    initial_message = "Hello, GLaDOS!"
    start_conversation_payload = {
        "content": initial_message
    }

    logger.info("Starting the conversation... Press Ctrl+C to end.")

    try:
        response = requests.post("http://localhost:5002/start_conversation", json=start_conversation_payload)
        response.raise_for_status()
        response_data = response.json()

        access_token = response_data["access_token"]
        conversation_id = response_data["conversation_id"]
        conversation_history = response_data["conversation_history"]

        logger.info("Conversation started successfully.")

    except requests.RequestException as e:
        logger.error(f"Error starting the conversation: {e}")
        return

    try:
        with sd.InputStream(samplerate=SAMPLERATE, blocksize=BLOCKSIZE, channels=1, dtype="int16", callback=audio_callback):
            while conversation_active:
                sd.sleep(1000) 
    except KeyboardInterrupt:
        logger.info("\nEnding the conversation.")
        conversation_active = False

if __name__ == "__main__":
    main()
