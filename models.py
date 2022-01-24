from enum import unique
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    admin = db.Column(db.Boolean, unique=False, default=False)
    plot_access = db.Column(db.Boolean, unique=False, default=False)

        
    def __init__(self, username, email, password, admin=False, plot_access=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin
        self.plot_access = plot_access

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)