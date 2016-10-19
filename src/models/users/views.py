from flask import Blueprint, render_template, request, session, url_for, redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
from src.models.users.errors import UserErrors
from src.models.users.user import User
import src.models.users.decorators as user_decorators

__author__ = 'Ian'


user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/alerts', methods=['GET', 'POST'])
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.validate_login(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors as e:
            return e.message

    return render_template("users/login.html") # send the user an error if their login was invalid


@user_blueprint.route('/register', methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors as e:
            return e.message

    return render_template("users/register.html") # send the user an error if their login was invalid


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home.html'))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_alerts():
    return redirect(url_for('.user_alerts'))


@user_blueprint.route('/new', methods=['POST', 'GET'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit= float(request.form['price_limit'])
        item = Item(name, url)
        item.save_to_mongo()
        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price() # This already saves to MongoDB

    # What happens if it's a GET request
    return render_template('alerts/new_alert.html')


