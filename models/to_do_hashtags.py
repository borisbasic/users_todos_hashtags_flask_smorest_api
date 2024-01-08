from db import db


class ToDoHashtagModel(db.Model):
    __tablename__ = "tdh"

    id = db.Column(db.Integer, primary_key=True)
    to_do_id = db.Column(db.Integer, db.ForeignKey("todos.id"))
    hashtag_id = db.Column(db.Integer, db.ForeignKey("hashtags.id"))
