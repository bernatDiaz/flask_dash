from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
        
    def __init__(self, username, email, password, id=None):
        if id is not None:
            self.id = str(id)
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def set_id(self, id):
        self.id = str(id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)