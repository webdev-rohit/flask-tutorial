from datetime import datetime
from main import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# With SQLAlchemy we can represent database structures as classes. Those classes are called as Models. Each class defined with SQLAlchemy is going to be a table in the DB
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=no-member
    username = db.Column(db.String(20), unique=True, nullable=False) # pylint: disable=no-member
    email = db.Column(db.String(120), unique=True, nullable=False) # pylint: disable=no-member
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # pylint: disable=no-member
    password = db.Column(db.String(60), nullable=False) # pylint: disable=no-member
    posts = db.relationship('Post', backref='author', lazy=True) # pylint: disable=no-member
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=no-member
    title = db.Column(db.String(20), unique=True, nullable=False) # pylint: disable=no-member
    dated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # pylint: disable=no-member
    content = db.Column(db.Text, nullable=False) # pylint: disable=no-member
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # pylint: disable=no-member

    def __repr__(self):
        return f"Post('{self.title}', '{self.dated}')"
