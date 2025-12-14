from flask import Flask, request, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)

swagger = Swagger(app)

@app.route('/api/books/<int:id>', methods=['GET'])
@swag_from('books.yml')
def get_book(id):
    """
    Получение книги по ID
    ---
    """
    return jsonify({
        "id": id,
        "title": f"Book {id}",
        "author": "Author Name"
    })

@app.route('/api/authors/', methods=['POST'])
@swag_from('authors.json')
def create_author():
    """
    Создание автора
    ---
    """
    data = request.json
    return jsonify({
        "id": 1,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name")
    }), 201

if __name__ == "__main__":
    app.run(debug=True)