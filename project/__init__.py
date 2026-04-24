from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import threading
from .main import start_monitor

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db.init_app(app)

    from .main import main
    app.register_blueprint(main)

    from .legacy import legacy
    app.register_blueprint(legacy, url_prefix='/legacy')

    start_monitor()

    return app