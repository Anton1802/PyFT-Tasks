import os
import datetime

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler


basedir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)

app.config.from_object('app.config.Config')

db: SQLAlchemy = SQLAlchemy(app)
bc: Bcrypt = Bcrypt(app)

bootstrap: Bootstrap5 = Bootstrap5(app)

lm: LoginManager = LoginManager()
lm.init_app(app)

bgs = BackgroundScheduler()
bgs.start()

@app.before_request
def init_database() -> None:
    db.create_all()

@app.before_request
def change_session_lifetime():
    session.permanent = True
    session.permanent_session_lifetime = datetime.timedelta(days=3)

from app import views, models
