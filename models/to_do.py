import datetime
from db import db


class ToDoModel(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    to_do = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date(), default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", back_populates="todos")
    hashtags = db.relationship(
        "HashtagModel", back_populates="todos", secondary="tdh", lazy="dynamic"
    )
