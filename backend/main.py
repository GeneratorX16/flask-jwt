from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

from db import db
from api import blueprint
from auth import auth_api

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Path(__file__).parent / "mydb.db"}'

    db.init_app(app)
    app.register_blueprint(blueprint)
    app.register_blueprint(auth_api)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)