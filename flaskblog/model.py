from datetime import datetime
from flaskblog import db

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class User(db.Model):
    """User of website"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    #Define relationship to posts
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<User user_id={} username={}>".format(self.user_id,
                                                        self.username)

class Post(db.Model):
    """Posts users uplaod"""
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Post post_id={} title={}>".format(self.post_id, self.title)

