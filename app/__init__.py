import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5

basedir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)

app.config.from_object('app.config.Config')

db: SQLAlchemy = SQLAlchemy(app)
bc: Bcrypt = Bcrypt(app)

bootstrap: Bootstrap5 = Bootstrap5(app)

@app.before_request
def init_database() -> None:
    db.create_all()

from app import views, models
