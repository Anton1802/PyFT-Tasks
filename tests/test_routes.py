import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app
from flask import session

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<h1>Welcome!</h1>" in response.data

def test_signin(client):
    response = client.get('/signin')
    assert response.status_code == 200
    assert b"""<div class="container" style="height: 80vh;">""" in response.data

def test_signup(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"""<div class="container" style="height: 80vh;">""" in response.data

def test_logout_redirect(client):
    response = client.get("/mytodo", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/signin"