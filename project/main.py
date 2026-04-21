from flask import render_template, Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/ping')
def keepalive():
    return jsonify(Status='OK'), 200