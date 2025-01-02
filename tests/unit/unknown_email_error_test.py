import pytest
from unittest.mock import patch

from gudlift import create_app


# Créé un client de test
@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


# Mock des données fictives
mocked_clubs = [
    {"name": "Test Success", "email": "test@success.com", "points": 10},
]


# Test le cas d'un email inconu
@patch('gudlift.routes.clubs', mocked_clubs)
def test_email_not_found(client):
    # Simule la soumission d'un formulaire avec un email inconnu
    response = client.post('/showSummary', data={'email': 'test@fail.com'})
    # Vérifie la redirection (302)
    assert response.status_code == 302
    # Récupère la réponse après la redirection (page d'accueil)
    response = client.get('/')
    # Vérifie que le message flash est bien dans la réponse
    assert b'Sorry, this email was not found.' in response.data


# Test le cas d'un email connu
@patch('gudlift.routes.clubs', mocked_clubs)
def test_email_found(client):
    # Simule la soumission d'un formulaire avec un email existant
    response = client.post('/showSummary', data={'email': 'test@success.com'})
    # Vérifie la réponse pour showSummary (200)
    assert response.status_code == 200
    # Vérifie que le message de bienvenue est dans la réponse
    assert b'Welcome, test@success.com' in response.data
