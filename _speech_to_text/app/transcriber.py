import speech_recognition as sr
import os


def transcribe_audio(audio_file_path):
    if not os.path.isfile(audio_file_path):
        return f"File not found: {audio_file_path}"

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

    except sr.UnknownValueError:
        return "Unable to understand the audio."
    except sr.RequestError as e:
        return f"Error accessing the speech recognition service: {e}"
    except Exception as e:
        return f"Unexpected error during transcription: {e}"
