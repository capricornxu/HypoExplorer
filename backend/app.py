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
        sent_dict = Iterator(grammar, 40)
        sentence_to_json(sent_dict, "sentence.json")

        return flask.Response(response=json.dumps(sent_dict), status=201)

hypo_string = """
    root -> hypo
    hypo -> expr '[' pred ']' op expr '[' pred ']'
    expr -> func '(' var ')' | var
    var -> attr | const
    pred -> var op const | pred '&' pred | 
    op -> '=' | '<'
    attr -> 'customer_id' | 'first_name' | 'last_name' | 'age' | 'country'
    const -> 'number' | 'string'
    func -> 'AVG' | 'MAX' | 'MIN' | 'COUNT'
    """

if __name__ == "__main__":
    grammar = CFG.fromstring(hypo_string)
    tree = findDeterministicTree(grammar)
    print("returned tree:")
    print(tree)
    app.debug = True
    app.run("localhost", 6969)

    