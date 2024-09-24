import os 
from decouple import config

basedir: str = os.path.abspath(os.path.dirname(__file__))

class Config():
    CSRF_ENABLED = True
    SECRET_KEY = config('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_TELEGRAM_BOT = config("TOKEN_TELEGRAM_BOT")
