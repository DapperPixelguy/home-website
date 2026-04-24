import json
import threading
import time

from flask import render_template, Blueprint, jsonify, request, Response
from datetime import datetime
from dotenv import load_dotenv
import os
from gevent import sleep

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/ping')
def keepalive():
    return jsonify(Status='OK'), 200

last_ping = datetime.now()
message = "This is a default message"
last_seen = None

@main.route('/status', methods=['POST'])
def status():
    global last_ping
    global message
    global last_seen

    if request.headers.get('X-Secret-Key') != SECRET_KEY:
        print('Request denied')
        return jsonify(Status='Unauthorized'), 401

    data = request.get_json()
    last_ping = datetime.now()
    last_seen = None
    try:
        message = data['message']
    except KeyError:
        pass
    return jsonify(Status='OK'), 200


def ping_monitor():
    global last_seen
    status_timeout_seconds = 10
    while True:
        timediff = datetime.now() - last_ping
        print(f'timediff: {timediff.total_seconds()}, last_seen: {last_seen}')
        if timediff.total_seconds() >= status_timeout_seconds:  # Has it been more than 60 seconds without a ping?
            if not last_seen:  # Set a last seen time for the start of each inactivity
                last_seen = datetime.now()
        sleep(1)

def start_monitor():
    threading.Thread(target=ping_monitor, daemon=True).start()

@main.route('/status-stream')
def status_stream():
    global last_ping
    global message

    def generate():
        global last_seen
        while True:
            if last_seen:
                seendiff = datetime.now() - last_seen

                if seendiff.total_seconds() <= 60:
                    x = seendiff.total_seconds().__floor__()
                    data = json.dumps({'status': 'offline', 'message': f'Last seen {x}s ago'})

                elif seendiff.total_seconds() <= 3600:
                    x = (seendiff.total_seconds() / 60).__floor__()
                    data = json.dumps({'status': 'offline', 'message': f'Last seen {x}m ago'})

                else:
                    x = (seendiff.total_seconds() / 60 / 60).__floor__()
                    data = json.dumps({'status': 'offline', 'message': f'Last seen {x}h ago'})

                yield f"data: {data}\n\n"

            else:
                data = json.dumps({'status': 'online', 'message': f'"{message}"'})
                yield f"data: {data}\n\n"
            sleep(1)

    return Response(generate(), mimetype='text/event-stream')