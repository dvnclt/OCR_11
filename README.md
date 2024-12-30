# OCR P11 - Gudlift

Ce projet est une application Flask pour la gestion des clubs sportifs et des compétitions. L'application permet aux utilisateurs de consulter les compétitions disponibles, réserver des places et afficher des informations sur les clubs.

## Structure du projet

Voici la structure des dossiers du projet :

OCR_P11/ │
 ├── gudlift/ 
 │  ├── init.py # Initialise l'application Flask 
 │  ├── routes.py # Contient l'ensemble des routes
 │  ├── utils.py # Contient les fonctions utilitaires comme loadClubs() et loadCompetitions() 
 │  └── templates/ # Contient les templates HTML
 │      ├── index.html 
 │      ├── welcome.html 
 │      └── booking.html 
 ├── config.py # Contient la configuration de l'application 
 └── run.py # Point d'entrée pour lancer l'application

## Installation

### Prérequis

- Python 3.x
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Clonez ce repository :
   ```bash
   git clone https://github.com/votre-utilisateur/OCR_P11.git
   cd OCR_P11

2. Créez un environnement virtuel :
    ```bash
    python3 -m venv venv

3. Activez l'environnement virtuel :
    Sur MacOS/Linux :
        ```bash
        source venv/bin/activate

    Sur Windows :
        ```bash
        .\venv\Scripts\activate

4. Installez les dépendances :
    ```bash
    pip install -r requirements.txt


### Fichiers JSON

Assurez-vous que les fichiers clubs.json et competitions.json sont présents dans le répertoire racine du projet ou ajustez les chemins dans le code pour pointer vers leur emplacement correct.

## Lancer l'application

1. Pour démarrer l'application, utilisez le fichier run.py :
    ```bash
    python run.py

2. L'application sera disponible à l'adresse http://127.0.0.1:5000/.


### Routes principales
/ : Page d'accueil (Index)
/showSummary : Affiche un résumé du club et des compétitions
/book/<competition>/<club> : Permet de réserver des places pour une compétition
/purchasePlaces : Confirme la réservation des places pour une compétition
/logout : Permet à l'utilisateur de se déconnecter
