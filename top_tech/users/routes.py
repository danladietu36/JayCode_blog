from flask import render_template, url_for, redirect, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from top_tech import db, bcrypt
from top_tech.models import Admin, Post
from top_tech.users.forms import (Registration_form, Login_form, Update_account)


users = Blueprint('users', __name__)


@users.route('register', methods=['GET', 'POST'], strict_slashes=False)
def register():