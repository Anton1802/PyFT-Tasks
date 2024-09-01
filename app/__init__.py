import os

from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

from app import views, models
