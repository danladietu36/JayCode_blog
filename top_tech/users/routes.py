from flask import render_template, url_for, redirect, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from top_tech import db, bcrypt
from top_tech.models import User, Post
from top_tech.users.forms import (Registration_form, Login_form, Update_account)
from top_tech import bcrypt, db
from top_tech.users.utils import save_photos

users = Blueprint('users', __name__)


@users.route('register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Registration_form()
    if form.validate_on_submit():
        hashed_passwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Email and Password incorrect', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('logout', strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('account', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_account():
    form = Update_account()
    if form.validate_on_submit():
        if form.profile_picture.data:
            pic_file = save_photos(form.profile_picture.Data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.add()
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.update_account'))
    elif request.method == 'GET':
        current_user.username.data = form.username
        current_user.email.data = form.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('update_account.html', title='Account', image_file=image_file, form=form)

@users.route('user/<string:username>', strict_slashes=False)
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_created)\
            .paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=posts, user=user)
