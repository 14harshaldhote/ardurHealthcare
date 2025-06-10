from flask_login import UserMixin
from ..utils.file_ops import read_json, write_json
from flask import current_app

class User(UserMixin):
    def __init__(self, username, email):
        self.id = username
        self.username = username
        self.email = email

    @staticmethod
    def get(username):
        users = read_json(current_app.config['USERS_FILE'])
        user_data = users.get(username)
        if user_data:
            return User(username=username, email=user_data['email'])
        return None
