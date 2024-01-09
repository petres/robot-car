import os
import json

from flask import Flask, jsonify
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
        'is_alive': r.isAlive()
    })

@app.route("/connect")
def connect():
    try:
        r.connect()
        return jsonify({
            'connected': True
        })
    except Exception as e:
        return jsonify({
            'connected': False,
            'error': str(e)
        })