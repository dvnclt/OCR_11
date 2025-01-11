import pytest

from gudlift import create_app


# Créé un client de test
@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_points_board_page(client):
    response = client.get('/pointsBoard')

    # Vérifie que la page se charge
    assert response.status_code == 200

    # Vérifie que le tableau des clubs est présent
    assert b'Points Display Board' in response.data
    assert b'Club Name' in response.data
    assert b'Available Points' in response.data
