from flask import Flask, request, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from
import json

app = Flask(__name__)

with open('authors.json', 'r', encoding='utf-8') as f:
    authors_spec = json.load(f)

swagger = Swagger(app)

# --- Книги (YAML-файл) ---
@app.route('/api/books/<int:id>', methods=['GET'])
@swag_from('books.yml')
def get_book(id):
    return jsonify({"id": id, "title": f"Book {id}", "author_id": 1})

@app.route('/api/books/<int:id>', methods=['PUT'])
@swag_from('books.yml')
def update_book(id):
    data = request.json or {}
    return jsonify({"message": "Book updated"}), 200

@app.route('/api/books/<int:id>', methods=['DELETE'])
@swag_from('books.yml')
def delete_book(id):
    return jsonify({"message": "Book deleted"}), 200

@app.route('/api/books/', methods=['POST'])
@swag_from('books.yml')
def create_book():
    data = request.json or {}
    return jsonify({"id": 1, "title": data.get("title"), "author_id": data.get("author_id")}), 201

@app.route('/api/authors/', methods=['POST'])
@swag_from(authors_spec)
def create_author():
    data = request.json or {}
    return jsonify({
        "id": 1,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "middle_name": data.get("middle_name")
    }), 201

@app.route('/api/authors/<int:id>', methods=['GET'])
@swag_from(authors_spec)
def get_author(id):
    return jsonify({
        "id": id,
        "first_name": "Абай",
        "last_name": "Кунанбаев",
        "middle_name": "Ибраһим",
        "books": [{"id": 1, "title": "Book 1"}]
    })

@app.route('/api/authors/<int:id>', methods=['DELETE'])
@swag_from(authors_spec)
def delete_author(id):
    return jsonify({"message": "Author and all books deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)