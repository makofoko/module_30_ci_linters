from flask import Flask, request, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from
from jsonrpcserver import method, dispatch

app = Flask(__name__)
swagger = Swagger(app, template_file='authors.json')


@app.route('/api/books/<int:id>', methods=['GET'])
@swag_from('books.yml')
def get_book(id):
    return jsonify({"id": id, "title": f"Book {id}", "author": "Author Name"})

@app.route('/api/authors/', methods=['POST'])
def create_author():
    data = request.json
    return jsonify({
        "id": 1,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name")
    }), 201

@app.route('/hello')
@swag_from('hello_endpoint.yaml')
def hello():
    return 'Привет, {}'.format(request.args.get('name', 'Мир'))

@app.route('/post_hello', methods=['POST'])
def post_hello():
    name = request.form.get('name', 'Мир')
    return 'Привет, {}'.format(name)


@method
def add(a: int, b: int) -> int:
    return a + b

@method
def sub(a: int, b: int) -> int:
    return a - b

@method
def mul(a: int, b: int) -> int:
    return a * b

@method
def div(a: int, b: int) -> float:
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return a / b

@app.route("/api", methods=["POST"])
def rpc():
    response = dispatch(request.get_data().decode())
    return response

if __name__ == "__main__":
    app.run(debug=True)