import os

from flask import render_template, request, url_for, redirect, send_from_directory

from app import app

@app.route('/')
def index():
    return "Hello World"
