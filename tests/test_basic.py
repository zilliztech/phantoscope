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


def local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
