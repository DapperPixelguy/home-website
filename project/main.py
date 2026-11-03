import json

from flask import render_template, Blueprint, jsonify, request, Response
from datetime import datetime
from dotenv import load_dotenv
import os
from gevent import sleep, spawn
from .extensions import redis_client

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/ping')
def keepalive():
    return jsonify(Status='OK'), 200


def set_val(key, val):
    redis_client.set(key, val)

def get_val(key):
    val = redis_client.get(key)
    if not val:
        return None
    else:
        return val.decode('utf-8')

def del_val(key):
    redis_client.delete(key)


@main.route('/status', methods=['POST'])
def status():
    if request.headers.get('X-Secret-Key') != SECRET_KEY:
        print('Request denied')
        return jsonify(Status='Unauthorized'), 401

    data = request.get_json()

    set_val('last_ping', datetime.now().isoformat())
    redis_client.delete('last_seen')
    new_message = data.get('message')
    if new_message:
        set_val('message', new_message)

    new_activity = data.get('activity')
    if new_activity != 'unchanged':
        if new_activity:
            set_val('activity', new_activity)
        else:
            del_val('activity')

    return jsonify(Status='OK'), 200


# Monitor incoming pings to determine whether to display a last seen status
def ping_monitor():
    status_timeout_seconds = 20
    while True:
        timediff = datetime.now() - datetime.fromisoformat(get_val('last_ping'))
        print(f'timediff: {timediff.total_seconds()}, last_seen: {get_val("last_seen")}')
        if timediff.total_seconds() >= status_timeout_seconds:  # Has it been more than 60 seconds without a ping?
            if not get_val('last_seen'):  # Set a last seen time for the start of each inactivity
                set_val('last_seen', datetime.now().isoformat())
        sleep(1)

def start_monitor():
    spawn(ping_monitor)


@main.route('/status-stream')
def status_stream():
    def generate():
        while True:
            last_seen = get_val('last_seen')
            if last_seen:
                seendiff = datetime.now() - datetime.fromisoformat(last_seen)

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
                data = json.dumps({'status': 'online',
                                   'message': f'"{get_val("message")}"',
                                   'activity': get_val('activity')
                                   })
                yield f"data: {data}\n\n"
            sleep(1)

    return Response(generate(), mimetype='text/event-stream')