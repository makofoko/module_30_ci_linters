from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, Namespace
from marshmallow import Schema, fields

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    books = db.relationship("Book", backref="author", cascade="all, delete-orphan")

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str()

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)
    author = fields.Nested(AuthorSchema, dump_only=True)

author_schema = AuthorSchema()
book_schema = BookSchema()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

api = Api(app, title="Library API", version="1.0", description="Books & Authors API")
book_ns = Namespace("books")
author_ns = Namespace("authors")

@book_ns.route("/<int:id>")
class BookResource(Resource):
    def get(self, id):
        book = Book.query.get_or_404(id)
        return book_schema.dump(book)

    def put(self, id):
        book = Book.query.get_or_404(id)
        data = request.json
        author = Author.query.get(data["author_id"])
        if not author:
            return {"error": "Author not found"}, 404
        book.title = data["title"]
        book.author_id = data["author_id"]
        db.session.commit()
        return {"message": "Book updated"}, 200

    def delete(self, id):
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}, 200

@author_ns.route("/")
class AuthorList(Resource):
    def post(self):
        data = request.json
        author = Author(**data)
        db.session.add(author)
        db.session.commit()
        return author_schema.dump(author), 201

@author_ns.route("/<int:id>")
class AuthorResource(Resource):
    def get(self, id):
        author = Author.query.get_or_404(id)
        return {
            "author": author_schema.dump(author),
            "books": [book_schema.dump(b) for b in author.books]
        }

    def delete(self, id):
        author = Author.query.get_or_404(id)
        db.session.delete(author)
        db.session.commit()
        return {"message": "Author and all books deleted"}, 200

api.add_namespace(book_ns, path="/api/books")
api.add_namespace(author_ns, path="/api/authors")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)