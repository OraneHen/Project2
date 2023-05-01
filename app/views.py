"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from . import app, db
from flask import render_template, request, jsonify, send_file, url_for, flash, session, abort, send_from_directory, make_response
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from flask_wtf.csrf import generate_csrf
from functools import wraps
from datetime import datetime, timedelta
from app.models import Posts, Likes, Follows, Users
from app.forms import RegisterForm, LoginForm, PostForm

import jwt
import os


# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)
        

        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401
        

        token = parts[1]
    
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        current_user = Users.query.filter_by(id = data['user_id']).first()
        
        return f(current_user, *args, **kwargs)

    return decorated


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/register', methods = ['POST'])
def register():
    if request.method=='POST':
        form = RegisterForm()
        if form.validate_on_submit():
            response = {}

            username = form.username.data
            password = form.password.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            location = form.location.data
            biography = form.biography.data
            profile_photo_data = form.photo.data
            profile_photo = secure_filename(profile_photo_data.filename)

            new_user= Users(username, password, firstname, lastname, email, location, biography, profile_photo)
            profile_photo_data.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_photo))
            db.session.add(new_user)
            db.session.commit()

            response = jsonify({"message": "User Successfully Added",
                                "username": username,
                                "first Name": firstname,
                                "last Name": lastname,
                                "password" :password,
                                "email" : email,
                                "location": location,
                                "biography":biography,
                                "photo": profile_photo})
                                
        
            return make_response(response,200)
        else:
            return make_response(jsonify({'errors': form_errors(form)}),400)

@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
    if request.method=='POST':
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = db.session.execute(db.select(Users).filter_by(username=username)).scalar()
            
            print(password)
       
            if user is not None and (check_password_hash(user.password, password)):
                timestamp = datetime.utcnow()
                payload = {
                    "sub": 1,
                    "iat": timestamp,
                    "exp": timestamp + timedelta(minutes=60),
                    "user_id": user.id
                }

                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            
                return make_response(jsonify({'token' : token, "username": user.username, "message": "Login Successful"}),201)
            return make_response(jsonify({"message": "Failed to login check you're credentials"}),201)
        else:
            return make_response({'errors': form_errors(form)},400)


@app.route('/api/v1/users/<user_id>/posts', methods = ['POST','GET'])
@requires_auth
def posts(current_user, user_id):
    if request.method=='POST':
        form = PostForm()
        if form.validate_on_submit():
            caption = form.caption.data
            photo = form.photo.data
            pname = secure_filename(photo.filename)
            newPost = Posts(caption, pname, current_user.id)
            db.session.add(newPost)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], pname))
            db.session.commit()

            return make_response({"message": "Successfully created a new post"},200)
        else:
            return make_response({'errors': form_errors(form)},400)
    
    elif request.method == 'GET':
        posts = Posts.query.filter_by(user_id=user_id).all()
        follows = Follows.query.filter_by(user_id=user_id).all()
        user = Users.query.filter_by(id=user_id).first()
        is_following = len(Follows.query.filter_by(user_id=user_id, follower_id = current_user.id).all()) > 0
        pList = []
        for post in posts:
            pList.append({
            "id": post.id,
            "user_id": post.user_id,
            "photo": "/api/v1/images/{}".format(post.photo),
            "caption": post.caption,
            "created_on": post.created_on
        })
    
        response =   jsonify({"posts": pList,  "user": {
                "is_current_user": current_user.id ==  int(user_id),
                "is_following" : is_following,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "location": user.location,
                "biography": user.biography,
                "joined_on": user.joined_on.strftime("%d %b %Y"),
                "posts": len(posts),
                "follows": len(follows),
                "user_profile": "/api/v1/images/{}".format(user.profile_photo),  
            }})
        return make_response(response,200)

@app.route('/api/v1/users/<user_id>/follow', methods = ['POST'])
@requires_auth
def follow(current_user, user_id):
    if request.method=='POST':
        if int(user_id) != current_user.id:
            existing_follows = Follows.query.filter_by(follower_id = current_user.id, user_id = user_id).all()
            if len(existing_follows) == 0:
                follower_id = current_user.id
                user_id = user_id
                newFollower = Follows(follower_id, user_id)
                db.session.add(newFollower)
                db.session.commit()
        return make_response({"message": "Successfully followed user"},200)



@app.route('/api/v1/posts', methods = ['GET'])
@requires_auth
def allPosts(current_user):
    posts = Posts.query.all()
    pList = []

    for post in posts:
        likes = len(Likes.query.filter_by(post_id=post.id).all())
        user = Users.query.filter_by(id = post.user_id).first()
        pList.append({
            "id": post.id,
            "user_id": post.user_id,
            "username": user.username,
            "user_profile": "/api/v1/images/{}".format(user.profile_photo),  
            "photo": "/api/v1/images/{}".format(post.photo),
            "caption": post.caption,
            "created_on": post.created_on.strftime("%d %b %Y"),
            "likes": likes
        })
    
    data = {"posts": pList}
    return jsonify(data)

@app.route('/api/v1/posts/<post_id>/like', methods = ['POST'])
@requires_auth
def like(current_user,post_id):
    if request.method=='POST':
        user_id = current_user.id
        post_id = post_id
        post = Posts.query.filter_by(id = post_id).first()
        if user_id != post.user_id:
            existing_likes = Likes.query.filter_by(post_id = post_id, user_id = user_id).all()
            if len(existing_likes) == 0:
                newLike= Likes(post_id, user_id)
                db.session.add(newLike)
                db.session.commit()
        return make_response({"message": "Successfully liked post"},200)
        


@app.route('/api/v1/images/<filename>')
def getProfilePhoto(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404