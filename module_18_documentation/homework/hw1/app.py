from flask import Flask, request, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/books/<int:id>', methods=['GET'])
@swag_from('books.yml')
def get_book(id):
    """Получить книгу по ID"""
    return jsonify({
        "id": id,
        "title": f"Book {id}",
        "author_id": 1
    })

@app.route('/api/books/', methods=['POST'])
@swag_from('books.yml')
def create_book():
    """Создать книгу"""
    data = request.json
    return jsonify({
        "id": 1,
        "title": data.get("title"),
        "author_id": data.get("author_id")
    }), 201

@app.route('/api/authors/', methods=['POST'])
@swag_from('authors.json')
def create_author():
    """Создать автора"""
    data = request.json
    return jsonify({
        "id": 1,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "middle_name": data.get("middle_name")
    }), 201

@app.route('/api/authors/<int:id>', methods=['GET'])
@swag_from('authors.json')
def get_author(id):
    """Получить автора по ID"""
    return jsonify({
        "id": id,
        "first_name": "Абай",
        "last_name": "Кунанбаев",
        "middle_name": "Ибраһим",
        "books": [{"id": 1, "title": "Book 1"}]
    })

@app.route('/api/authors/<int:id>', methods=['DELETE'])
@swag_from('authors.json')
def delete_author(id):
    """Удалить автора по ID"""
    return jsonify({"message": "Author and all books deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)