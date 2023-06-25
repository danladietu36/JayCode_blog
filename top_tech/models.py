from datetime import datetime
from itsdangerous import TimedSerializer
from top_tech import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(20), nullabe=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.image_file}')"


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    certificates = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f"Admin('{self.username}', '{self.image_file}', '{self.posts}')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __repr__(self):
        return f" Post('{self.title}', '{self.date_created}')"