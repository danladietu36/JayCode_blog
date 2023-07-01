from flask import render_template, url_for, redirect, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from top_tech import db, bcrypt
from top_tech.models import User, Post
from top_tech.users.forms import (Registration_form, Login_form, Update_account)
from top_tech import bcrypt, db


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

