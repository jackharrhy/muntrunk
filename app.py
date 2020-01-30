from flask import Flask, jsonify
from muntrunk.parse import parse_entire_list

app = Flask(__name__)


@app.route("/")
def get_entire_list():
    return jsonify(parse_entire_list())


if __name__ == "__main__":
    for course in parse_entire_list()["courses"]:
        print(course)
