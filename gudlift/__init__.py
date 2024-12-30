from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Importe les routes après la création de l'application
    from . import routes
    app.register_blueprint(routes.bp)

    return app
