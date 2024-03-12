import os
import json
import time

from flask import Flask, jsonify, request, send_file, Response
from robot import Robot
from camera import Camera

app = Flask(__name__)

with open(os.path.join(app.instance_path, 'config.json')) as f:
    config = json.load(f)
        
r = Robot(config['host'], config['api']['port'])
c = Camera(f"http://{config['host']}:{config['stream']['port']}/{config['stream']['path']}")

@app.route("/")
def home():
    return get_status()

@app.route("/config")
def get_config():
    return jsonify(config)

@app.route("/status")
def get_status():
    return jsonify({
        'is_alive': r.isAlive(),
        'is_streaming': c.isStreaming(),
        'messages': r.recv_q.qsize()
    })

@app.route("/connect")
def connect():
    try:
        c.connect()
        if not r.isAlive():
            r.disconnect()
            r.connect()
            
        return jsonify({
            'valid': True
        })
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        })

@app.route("/disconnect")
def disconnect():
    try:
        r.disconnect()
        c.disconnect()
        return jsonify({
            'valid': True
        })
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        })

@app.route("/send", methods=['POST'])
def send():
    try:
        message = request.json.get('message')
        r.send(message + "\n")
        return jsonify({
            'valid': True
        })
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        })

@app.route("/log", methods=['GET'])
def log():
    return send_file(os.path.join(app.instance_path, 'robot.log'))






@app.route('/stream')
def stream():
    def gen():
        while True:
            time.sleep(0.03)
            frame = c.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

import io
@app.route('/img')
def img():
    return send_file(
        io.BytesIO(c.get_frame()),
        mimetype='image/jpeg',
        download_name='img.jpg' 
    )



