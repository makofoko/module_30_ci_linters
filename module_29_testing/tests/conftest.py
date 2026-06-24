import pytest
from module_29_testing.hw import create_app, db

@pytest.fixture
def app():
    app = create_app("testing")
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def _db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
