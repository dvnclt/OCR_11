import json


MAX_PLACES = 12


def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']


def saveClubs(clubs):
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=4)


def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


def saveCompetitions(competitions):
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)
