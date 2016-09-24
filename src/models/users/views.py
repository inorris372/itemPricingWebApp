from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

from src.models.users.user import User

__author__ = 'Ian'


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', "POST"])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.validate_login(email, password):
            session['email'] = email
            return redirect(url_for(".user_alerts"))

    return render_template("users/login.html") # send the user an error if their login was invalid


@user_blueprint.route('/register')
def register_user():
    pass


@user_blueprint.route('/alerts')
def user_alerts():
    pass


@user_blueprint.route('/logout')
def logout_user():
    pass


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass


