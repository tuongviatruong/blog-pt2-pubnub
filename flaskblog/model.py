from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User of website"""

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    #Define relationship to posts
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<User user_id={} username={} email={}>".format(self.id,
                                                        self.username, self.email)

class Post(db.Model):
    """Posts users uplaod"""

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Post post_id={} title={} date={}>".format(self.id, self.title, self.date_posted)

