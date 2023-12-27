from . import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    login = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    avatar_path = db.Column(db.String(100))
    id_post = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean, default=False)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_author = db.Column(db.Integer)
    text = db.Column(db.String(300))
    img_path = db.Column(db.String(100))

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    id_post = db.Column(db.Integer)
    score = db.Column(db.Integer)

