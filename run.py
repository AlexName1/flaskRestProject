from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_object("config")

    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from Model import db
    db.init_app(app)

    from migrate import migrate
    migrate.init_app(app, db)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
