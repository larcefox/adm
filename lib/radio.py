from flask import Flask, Response
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)
# URL of the radio station stream
radio_8bit = "http://myradio24.org/85516"

@app.route('/8bit')
def stream_audio():
    def generate():
        with requests.get(radio_8bit, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
    
    return Response(generate(), content_type="audio/mpeg")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8100)
