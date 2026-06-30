from datetime import datetime

from flask import Flask
from .main import start_monitor
import os


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['REDIS_URL'] = os.getenv('REDIS_URL')

    from .extensions import db
    db.init_app(app)

    from .extensions import redis_client
    redis_client.init_app(app)
    redis_client.set('last_ping', datetime.now().isoformat())
    redis_client.set('message', 'Hello! Thanks for visiting :)')

    from .main import main
    app.register_blueprint(main)

    from .legacy import legacy
    app.register_blueprint(legacy, url_prefix='/legacy')

    start_monitor()

    return app