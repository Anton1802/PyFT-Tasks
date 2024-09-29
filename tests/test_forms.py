import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_signin_form(client):
    form_data = {'username': 'john', 'password': 'password'}
    response = client.post('/signin', data=form_data)
    assert response.status_code == 200

def test_signup_form(client):
    form_data = {'username': 'john', 'password': 'password'}
    response = client.post('/signup', data=form_data)
    assert response.status_code == 200

