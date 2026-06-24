from flask import Flask
from .extensions import db
from .config import Config, TestingConfig

def create_app(config_name="default"):
    app = Flask(__name__)

    if config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from . import models
        from .routes import bp
        app.register_blueprint(bp)
        db.create_all()

    return app
