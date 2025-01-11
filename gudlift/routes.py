from flask import Blueprint, render_template, request, flash, redirect, url_for
from .utils import (loadClubs, loadCompetitions, saveClubs, saveCompetitions,
                    MAX_PLACES)
from datetime import datetime

# Crée un blueprint pour les routes
bp = Blueprint('main', __name__)

clubs = loadClubs()
competitions = loadCompetitions()


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)

    if club is None:
        flash("Sorry, this email was not found.", "error")
        return redirect(url_for('main.index'))

    # Vérifie et ajoute l'attribut is_past pour chaque compétition
    for competition in competitions:
        competition_date = datetime.strptime(competition['date'],
                                             "%Y-%m-%d %H:%M:%S")
        competition['is_past'] = competition_date < datetime.now()

    return render_template('welcome.html', club=club,
                           competitions=competitions)


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    # Recherche la compétition et le club correspondants
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] ==
                             competition), None)

    if not foundClub or not foundCompetition:
        flash("Something went wrong - please try again.", "error")
        return render_template('welcome.html', club=None,
                               competitions=competitions)

    # Vérifie si la compétition donnée est terminée
    competition_date = datetime.strptime(foundCompetition['date'],
                                         "%Y-%m-%d %H:%M:%S")
    foundCompetition['is_past'] = competition_date < datetime.now()

    # Si la compétition est passée, affiche un message d'erreur
    if foundCompetition['is_past']:
        flash("This competition has already ended.", "error")
        return render_template('welcome.html', club=foundClub,
                               competitions=competitions)

    # Si non, permet d'accéder à la réservation
    return render_template('booking.html', club=foundClub,
                           competition=foundCompetition)


@bp.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] ==
                   request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    points = int(club['points'])
    placesRequired = int(request.form['places'])

    # Vérifie que le nombre demandé est positif et logique
    if placesRequired <= 0:
        flash('Invalid number of places requested.')

    # Vérifie que le nombre de places demandé est <= au nombre de places disponible  # noqa: E501
    elif placesRequired > int(competition['numberOfPlaces']):
        flash('Not enough places available.')

    # Vérifie que le nombre de places demandés ne dépasse pas la limite
    elif placesRequired > MAX_PLACES:
        flash(f'You can not redeem more than {MAX_PLACES} places.')

    # Vérifie que le nombre de points est suffisant
    elif points < placesRequired:
        flash('Not enough points to book this number of places.')

    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired  # noqa: E501
        club['points'] = points - placesRequired
        flash('Great-booking complete !')

        saveClubs(clubs)
        saveCompetitions(competitions)

    return render_template(
        'welcome.html', club=club, competitions=competitions)


@bp.route('/pointsBoard')
def pointsBoard():
    return render_template('points_board.html', clubs=clubs)


@bp.route('/logout')
def logout():
    return redirect(url_for('main.index'))
