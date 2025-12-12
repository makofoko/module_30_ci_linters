from flask_restx import Api, Resource, Namespace
from flask import request
from models import db, Book, Author
from schemas import BookSchema, AuthorSchema

api = Api()
book_ns = Namespace("books")
author_ns = Namespace("authors")

book_schema = BookSchema()
author_schema = AuthorSchema()

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