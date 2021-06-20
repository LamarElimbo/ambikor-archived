from flask import redirect, render_template, url_for, Blueprint, session
from app import app, mongo
from app.views import _helpers


auth_blueprint = Blueprint('auth', __name__)


###################################################
################## LOGIN/LOGOUT ###################
###################################################

@auth_blueprint.route('/login_form')
def login_form():
    try:
        return render_template('account/login_form.html', skeleton=_helpers.get_skeleton())
    except:
        return render_template('errors/500.html')


@auth_blueprint.route('/login')
def user_login():
    if 'user_email' in session:
        return redirect(url_for('home.home_page'))
    login_user = mongo.db.users.find_one({'email' : 'fake_user@hotmail.com'})
    session['user_email'] = 'fake_user@hotmail.com'
    return redirect(url_for('home.home_page'))


@auth_blueprint.route("/logout")
def logout():
    try:
        session.pop('user_email', None)
        return redirect(url_for('home.home_page'))
    except:
        return render_template('errors/500.html')