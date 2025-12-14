from flask import Flask, request, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from
from models import db
from routes import book_ns, author_ns
from flask_restx import Api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

swagger = Swagger(app, template_file='authors.json')

api = Api(app)
api.add_namespace(book_ns, path="/api/books")
api.add_namespace(author_ns, path="/api/authors")

@app.route('/api/books/<int:id>', methods=['GET'])
@swag_from('books.yml')
def get_book(id):
    return jsonify({
        "id": id,
        "title": f"Book {id}",
        "author": "Author Name"
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)