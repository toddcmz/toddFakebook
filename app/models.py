from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login
from secrets import token_urlsafe

@login.user_loader # this is built in to our instance of our login manager instanced in our overall init
def load_user(user_id): # now we're going to get our user by our passed in ID, looking it up in table
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    token = db.Column(db.String(250), unique=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'User {self.username}'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(self, password):
        return generate_password_hash(password)
    
    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
    
    def add_token(self):
        setattr(self,'token', token_urlsafe(32) )
    
    def get_id(self):
        return str(self.user_id)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f'Post {self.body}'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()