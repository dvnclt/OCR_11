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
        "name": "Summer Showdown",
        "date": "2021-06-15 09:00:00",
        "numberOfPlaces": "5"
    },
    {
        "name": "Winter Cup",
        "date": "2021-12-05 14:00:00",
        "numberOfPlaces": "20"
    }
]


# Vérifie la validité du nombre de places demandé (<=0)
@patch('gudlift.routes.clubs', mocked_clubs)
@patch('gudlift.routes.competitions', mocked_competitions)
def test_invalid_places_number(client):
    # Simule la soumission d'un formulaire avec un nombre de places invalide (0)  # noqa: E501
    response = client.post('/purchasePlaces', data={
        'competition': 'Summer Showdown',
        'club': 'Powerhouse Gym',
        'places': '0'
    })
    # Vérifie que le message flash est bien dans la réponse
    assert b'Invalid number of places requested.' in response.data


# Vérifie la disponibilité du nombre de place demandé
@patch('gudlift.routes.clubs', mocked_clubs)
@patch('gudlift.routes.competitions', mocked_competitions)
def test_not_enough_places(client):
    # Cas où nombre de places demandé > nombre de places disponible
    response = client.post('/purchasePlaces', data={
        'competition': 'Summer Showdown',
        'club': 'Powerhouse Gym',
        'places': '6'
    })
    # Vérifie que le message flash est bien dans la réponse
    assert b'Not enough places available.' in response.data


# Vérifie que places <= au nombre de place limite
@patch('gudlift.routes.clubs', mocked_clubs)
@patch('gudlift.routes.competitions', mocked_competitions)
def test_too_many_places(client):
    # Cas où nombre de places demandé > MAX_PLACES
    response = client.post('/purchasePlaces', data={
        'competition': 'Winter Cup',
        'club': 'Powerhouse Gym',
        'places': '13'
    })
    # Vérifie que le message flash est bien dans la réponse
    assert b'You can not redeem more than 12 places.' in response.data


# Vérifie que le nombre de points est suffisant
@patch('gudlift.routes.clubs', mocked_clubs)
@patch('gudlift.routes.competitions', mocked_competitions)
def test_not_enough_points(client):
    # Cas où nombre de points insuffisant
    response = client.post('/purchasePlaces', data={
        'competition': 'Winter Cup',
        'club': 'Powerhouse Gym',
        'places': '6'
    })
    assert b'Not enough points to book this number of places.' in response.data


# Vérifie si la réservation a bien aboutie
@patch('gudlift.routes.clubs', mocked_clubs)
@patch('gudlift.routes.competitions', mocked_competitions)
@patch('gudlift.routes.saveClubs')
@patch('gudlift.routes.saveCompetitions')
def test_successful_booking(mock_save_clubs, mock_save_competitions, client):
    # Simule une réservation réussie
    response = client.post('/purchasePlaces', data={
        'competition': 'Summer Showdown',
        'club': 'Powerhouse Gym',
        'places': '5'
    })
    assert b'Great! You have successfully booked' in response.data
