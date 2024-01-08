from db import db


class HashtagModel(db.Model):
    __tablename__ = "hashtags"

    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(30), unique=True, nullable=False)
    todos = db.relationship(
        "ToDoModel", back_populates="hashtags", secondary="tdh", lazy="dynamic"
    )
