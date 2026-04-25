from flask_login import UserMixin
from app.extensions import db

class User(UserMixin,db.Model):
    __tablename__ = "Users"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    image = db.Column(db.String)
