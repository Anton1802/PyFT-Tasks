from flask_login import UserMixin
from sqlalchemy.types import DateTime
from app import db

class User(UserMixin, db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True, nullable=False)
    password: str = db.Column(db.String(500), nullable=False)

    def __init__(self, username, password) -> None:
        self.username: str = username
        self.password: str = password

    def __repr__(self) -> str:
        return str(self.id) + ' - ' + str(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Task(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    dat_success: DateTime = db.Column(db.DateTime, nullable=False)
    user_id: int = db.Column(db.Integer, nullable=False)

    def __init__(self, name, description, dat_success, user_id) -> None:
        self.name: str = name
        self.description: str = description
        self.dat_success: DateTime = dat_success
        self.user_id: int = user_id 
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self, name, description, dat_success, user_id):
        self.name: str = name
        self.description: str = description
        self.dat_success: DateTime = dat_success
        self.user_id = user_id
        
        db.session.commit()

        return self


class Notice(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    chat_id: str = db.Column(db.String(100), nullable=False)
    interval: str = db.Column(db.Integer, nullable=False)
    user_id: int = db.Column(db.Integer, nullable=False)

    def __init__(self, chat_id, interval, user_id) -> None:
        self.chat_id = chat_id
        self.interval = interval
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, chat_id, interval, user_id):
        self.chat_id = chat_id
        self.interval = interval
        self.user_id = user_id

        db.session.commit()

        return self