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
    {
        "name": "Powerhouse Gym",
        "email": "mike@powerhousegym.com",
        "points": "5"
    }
]
mocked_competitions = [
    {
        "name": "Past Competition",
        "date": "2021-06-15 09:00:00",
        "numberOfPlaces": "5"
    },
    {
        "name": "Future Competition",
        "date": "2050-01-10 14:00:00",
        "numberOfPlaces": "20"
    }
]


# Vérifie l'impossibilité de réserver pour une compétition passée
@patch("gudlift.routes.clubs", mocked_clubs)
@patch("gudlift.routes.competitions", mocked_competitions)
def test_booking_past_competition(client):
    response = client.get('/book/Past%20Competition/Powerhouse%20Gym')
    assert b'This competition has already ended.' in response.data


# Vérifie la possibilité de réserver pour une compétition future
@patch("gudlift.routes.clubs", mocked_clubs)
@patch("gudlift.routes.competitions", mocked_competitions)
def test_booking_future_competition(client):
    response = client.get('/book/Future%20Competition/Powerhouse%20Gym')
    assert b'How many places?' in response.data
