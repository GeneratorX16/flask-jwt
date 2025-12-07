from flask import Flask
from pathlib import Path
from flask_cors import CORS

from utils import get_redis_connector
from db import db
from auth import auth_api



def create_app():
    app = Flask(__name__)
    CORS(app, 
     resources={r"/*": {"origins": "*"}}, 
     supports_credentials=False 
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Path(__file__).parent / "mydb.db"}'

    db.init_app(app)
    app.register_blueprint(auth_api)

    # check redis connection
    r = get_redis_connector()

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)