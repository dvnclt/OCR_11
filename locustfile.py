from locust import HttpUser, task, between
from unittest.mock import patch

import random


class WebsiteUser(HttpUser):
    # Temps d'attente entre chaque requête (1 à 3 secondes)
    wait_time = between(1, 3)

    host = "http://localhost:5000"

    # Données de test
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        }
    ]
    competitions = [
        {
            "name": "Fake Tech Fair",
            "date": "2025-03-15 09:00:00",
            "numberOfPlaces": "50",
        },
        {
            "name": "Fake Sports Championship",
            "date": "2025-09-10 15:00:00",
            "numberOfPlaces": "20",
        }
    ]

    # Simule la fonction de sauvegarde
    def mock_save(data, file_path):
        return data

    @task
    def index(self):
        # Test la route d'accueil
        self.client.get("/")

    @task
    def show_summary(self):
        # Simule un utilisateur entrant un email valide pour se connecter
        club = random.choice(self.clubs)
        self.client.post("/showSummary", data={"email": club["email"]})

    @task
    def book_competition(self):
        # Simule la réservation d'une compétition par un club
        club = random.choice(self.clubs)
        competition = random.choice(self.competitions)
        self.client.get(f"/book/{competition['name']}/{club['name']}")

    @task
    @patch('gudlift.routes.saveClubs', mock_save)
    @patch('gudlift.routes.saveCompetitions', mock_save)
    def purchase_places(self):
        # Simule l'achat de places pour une compétition
        club = random.choice(self.clubs)
        competition = random.choice(self.competitions)
        self.client.post("/purchasePlaces", data={
            "competition": competition["name"],
            "club": club["name"],
            "places": random.randint(1, 12)
        })

    @task
    def points_board(self):
        # Test la route du tableau des points
        self.client.get("/pointsBoard")

    @task
    def logout(self):
        # Test la déconnexion
        self.client.get("/logout")
