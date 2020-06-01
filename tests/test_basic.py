import pytest
from main import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def db():
    from service import db
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
