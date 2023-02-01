from flask import Flask, request
import flask
import json
from flask_cors import CORS
from funcs import *

app = Flask(__name__)
CORS(app)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/", methods = ["GET", "POST"])
@app.route('/users', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")

    if request.method == "GET":
        with open("sentence.json", "r") as f:
            data = json.load(f)
            return flask.jsonify(data)
    
    if request.method == "POST":
        received_data = request.get_json()
        # process input grammar
        hypo_string = received_data
        grammar = CFG.fromstring(hypo_string)
        sent_dict = Iterator(grammar, 10)
        sentence_to_json(sent_dict, "sentence.json")

        return flask.Response(response=json.dumps(sent_dict), status=201)

if __name__ == "__main__":
    app.debug = True
    app.run("localhost", 6969)

    