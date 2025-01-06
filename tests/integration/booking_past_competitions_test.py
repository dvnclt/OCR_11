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
        "date": "2025-01-10 14:00:00",
        "numberOfPlaces": "20"
    }
]


# Vérifie l'impossibilité de réserver pour une compétition passée
@patch("gudlift.routes.competitions")
@patch("gudlift.routes.clubs")
def test_booking_past_competition(mock_clubs, mock_competitions, client):
    mock_clubs.return_value = mocked_clubs
    mock_competitions.return_value = mocked_competitions

    response = client.get('/book/Past%20Competition/Powerhouse%20Gym')
    assert b'Past Competition' in response.data
