import sys
import os
sys.path.insert(0, os.getcwd() + '/glados_tts')

import torch
from utils.tools import prepare_text
from scipy.io.wavfile import write
import time

from glados import tts_runner

print("\033[1;94mINFO:\033[;97m Initializing TTS Engine...")

glados = tts_runner(False, True)

def glados_tts(text, key=False, alpha=1.0):
    output_file = 'audio/GLaDOS-tts-temp-output.wav'
    if key:
        output_file = f'audio/GLaDOS-tts-temp-output-{key}.wav'

 
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    glados.run_tts(text, alpha).export(output_file, format="wav")
    return True



if __name__ == "__main__":

    PORT = 8124
    CACHE = True

    from flask import Flask, request, send_file
    import urllib.parse
    import shutil

    print("\033[1;94mINFO:\033[;97m Initializing TTS Server...")

    app = Flask(__name__)

    @app.route('/synthesize/', defaults={'text': ''})
    @app.route('/synthesize/<path:text>')
    def synthesize(text):
        if text == '':
            return 'No input'

        line = urllib.parse.unquote(request.url[request.url.find('synthesize/') + 11:])
        filename = "GLaDOS-tts-" + line.replace(" ", "-")
        filename = filename.replace("!", "")
        filename = filename.replace("°c", "degrees celcius")
        filename = filename.replace(",", "") + ".wav"
        file = os.getcwd() + '/audio/' + filename

        
        if os.path.isfile(file):
           
            os.utime(file, None)
            print("\033[1;94mINFO:\033[;97m The audio sample sent from cache.")
            return send_file(file)

        
        key = str(time.time())[7:]
        if glados_tts(line, key):
            tempfile = os.getcwd() + f'/audio/GLaDOS-tts-temp-output-{key}.wav'

           
            if len(line) < 200 and CACHE:
                shutil.move(tempfile, file)
            else:
                return send_file(tempfile)
                os.remove(tempfile)

            return send_file(file)

        else:
            return 'TTS Engine Failed'

    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app.run(host="0.0.0.0", port=PORT)