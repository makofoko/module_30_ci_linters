from flask import Flask
from db import init_db
from routes import bp

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)