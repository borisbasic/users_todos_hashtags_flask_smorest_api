from db import db

class Blocklist(db.Model):
    __tablename__ = 'blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))