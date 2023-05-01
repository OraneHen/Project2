from . import db
from werkzeug.security import generate_password_hash

class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    caption = db.Column(db.String(80))
    photo = db.Column(db.String(256))
    created_on = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, caption, photo, user_id):
        self.caption = caption
        self.photo = photo
        self.user_id = user_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<post: %r>' % (self.id)

class Likes(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<like: %r>' % (self.id)


class Follows(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, follower_id, user_id):
        self.follower_id = follower_id
        self.user_id = user_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<follows: %r>' % (self.id)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    location = db.Column(db.String(125))
    biography = db.Column(db.String(256))
    profile_photo = db.Column(db.String(256))
    joined_on = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username = username 
        self.password = generate_password_hash(password, method='pbkdf2:sha256') 
        self.first_name = firstname 
        self.last_name = lastname 
        self.email = email 
        self.location = location 
        self.biography = biography 
        self.profile_photo = profile_photo 

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)