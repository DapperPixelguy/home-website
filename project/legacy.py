import os

from flask import render_template, Blueprint, jsonify, send_from_directory

legacy = Blueprint('legacy', __name__)
LEGACY_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'legacy')


@legacy.route('/', defaults={'path': 'index.html'})
@legacy.route('/<path:path>')
def index(path):
    return send_from_directory(LEGACY_FOLDER, path)