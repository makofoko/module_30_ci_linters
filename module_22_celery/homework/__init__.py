from flask import Flask
from .celery_app import celery_app

def create_app():
    app = Flask(__name__)
    return app
