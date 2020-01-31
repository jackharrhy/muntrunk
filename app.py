from flask import Flask, jsonify
from muntrunk.parse import parse_w2020

app = Flask(__name__)


@app.route("/")
def get_entire_list():
    return jsonify(parse_w2020())
