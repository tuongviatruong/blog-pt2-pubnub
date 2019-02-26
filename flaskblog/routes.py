import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.model import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def homepage():
    """Show homepage with one blog already shown, show all in database after creating post"""
    # posts = Blog.query.all()
    return render_template("homepage.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homepage'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


def save_picture(form_picture):
    """Function to save image with random name + file_extention and resize """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# @app.route('/create', methods=['GET', 'POST'])
# def create_form():
#     """"Create a post and add to database"""
#     form = BlogForm()
#     if form.validate_on_submit():
#         post = Blog(title=form.title.data,description=form.description.data,date=form.date.data)
#         db.session.add(post)
#         db.session.commit()
#         return redirect('/')
#     return render_template("create_form.html", title="Create a Post", form=form)


# @app.route('/post/<int:blog_id>')
# def post(blog_id):
#     """Shows one post when clicked"""
#     post = Blog.query.get(blog_id)

#     return render_template('post.html', post=post)

# @app.route('/post/<int:blog_id>/edit', methods=["GET", "POST"])
# def edit_post(blog_id):
#     """Edit post with data and edit database"""
#     post = Blog.query.get(blog_id)

#     form = BlogForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.description = form.description.data
#         post.date= form.date.data
#         db.session.commit()
#         return redirect(url_for('post', blog_id=post.blog_id))

#     form.title.data = post.title
#     form.description.data = post.description
#     form.date.data = post.date

#     return render_template("create_form.html", title="Edit Post", form=form)
