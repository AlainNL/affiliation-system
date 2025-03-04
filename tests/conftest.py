import pytest
from app import create_app


@pytest.fixture
def app():
    """Crée une application Flask pour les tests."""
    app = create_app({
        'TESTING': True,
        'DEBUG': False
    })
    yield app


@pytest.fixture
def client(app):
    """Crée un client de test Flask."""
    return app.test_client()
