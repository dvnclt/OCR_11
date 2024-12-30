from gudlift import create_app

# Créer l'application Flask
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
