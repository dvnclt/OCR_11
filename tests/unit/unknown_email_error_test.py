import sys
import os
import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    )
from run import app  # noqa: E402


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_email_not_found(client):
    # Simule une soumission de formulaire avec un email inconnu
    response = client.post(
        '/showSummary', data={'email': 'unknown@example.com'}
        )
    # Vérifie la redirection (302)
    assert response.status_code == 302
    # Récupère la réponse après la redirection (page d'accueil)
    response = client.get('/')
    # Vérifie que le message flash est dans la réponse
    assert b'Sorry, this email was not found.' in response.data


def test_email_found(client):
    # Simule une soumission de formulaire avec un email existant
    response = client.post(
        '/showSummary', data={'email': 'admin@irontemple.com'}
        )
    # Vérifie la réponse pour '/showSummary' (200)
    assert response.status_code == 200
    # Vérifie que le message de bienvenue est dans la réponse
    assert b'Welcome, admin@irontemple.com' in response.data
