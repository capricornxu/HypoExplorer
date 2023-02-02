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
        hypo_string = received_data
        grammar = CFG.fromstring(hypo_string)
        tree_dict = findDeterministicTree(grammar)
        sent_dict = Iterator(grammar, 40)

        dict_list = [tree_dict, sent_dict]
        sentence_to_json(dict_list, "sentence.json")

        return flask.Response(response=json.dumps(dict_list, indent = 2), status=201)

if __name__ == "__main__":
    app.debug = True
    app.run("localhost", 6969)

    