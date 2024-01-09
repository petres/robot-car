import os
import json

from flask import Flask, jsonify, request
from robot import Robot

app = Flask(__name__)

with open(os.path.join(app.instance_path, 'config.json')) as f:
    config = json.load(f)
        
r = Robot(config['host'], config['api']['port'])

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
        'messages': r.got_q.qsize()
    })

@app.route("/connect")
def connect():
    try:
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
    print('send')
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
