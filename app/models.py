from app import db
from flask import current_app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(120), index=True, unique=True)
    short_url = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Url {}, {}>'.format(self.long_url, self.short_url)
