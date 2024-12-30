from flask import Blueprint, render_template, request, flash, redirect, url_for
from .utils import loadClubs, loadCompetitions

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

    return render_template('welcome.html', club=club,
                           competitions=competitions)


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@bp.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] ==
                   request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces']
        ) - placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display


@bp.route('/logout')
def logout():
    return redirect(url_for('main.index'))
