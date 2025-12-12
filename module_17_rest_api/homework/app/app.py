from flask import Flask
from models import db
from routes import api, book_ns, author_ns

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
api.init_app(app)

# регистрируем namespaces
api.add_namespace(book_ns, path="/api/books")
api.add_namespace(author_ns, path="/api/authors")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
