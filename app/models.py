from enum import unique
from sqlalchemy.orm import Mapped, mapped_column
from app import db

class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True)
    password: str = db.Column(db.String(500))

    def __init__(self, username, password) -> None:
        self.username: str = username
        self.password: str = password

    def __repr__(self) -> str:
        return str(self.id) + ' - ' + str(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
