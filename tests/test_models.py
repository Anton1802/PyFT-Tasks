import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import db
from app import app

from app.models import User, Task, Notice

from datetime import datetime

@pytest.fixture
def app_context():
    with app.app_context():
        yield

@pytest.fixture
def db_session(app_context):
    db.create_all()
    yield db.session
    db.session.remove()
    db.drop_all()

def test_user_model(db_session):
    user = User(username='Anton', password="passwordexample333")
    db_session.add(user)
    db_session.commit()
    assert user.username == 'Anton'
    assert user.password == 'passwordexample333'

def test_user_model(db_session):
    user = User(username='Anton', password="passwordexample333")
    db_session.add(user)
    db_session.commit()
    assert user.username == 'Anton'
    assert user.password == 'passwordexample333'

def test_task_model(db_session):
    date_t = datetime.now()
    task = Task(
        name="TaskExample",
        description="Description...", 
        dat_success=date_t,
        user_id=1,
    )
    db_session.add(task)
    db_session.commit()
    assert task.name == "TaskExample"
    assert task.description == "Description..."
    assert task.dat_success == date_t
    assert task.user_id == 1

def test_notice_model(db_session):
    notice = Notice(chat_id="2342423424", interval=10, user_id=1)
    db_session.add(notice)
    db_session.commit()
    assert notice.chat_id == "2342423424"
    assert notice.interval == 10
    assert notice.user_id == 1