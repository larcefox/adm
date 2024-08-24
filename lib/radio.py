from flask import Flask, Response
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)
# URL of the radio station stream
radio_8bit = "http://myradio24.org/85516"
radio_ambient = "http://ice6.somafm.com/deepspaceone-128-aac"

@app.route('/8bit')
def stream_radio_8bit():
    def generate():
        with requests.get(radio_8bit, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
    
    return Response(generate(), content_type="audio/mpeg")

@app.route('/ambient')
def stream_radio_ambient():
    def generate():
        with requests.get(radio_ambient, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
    
    return Response(generate(), content_type="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100)
