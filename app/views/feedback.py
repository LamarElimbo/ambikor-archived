###############################################
################## FEEDBACK ###################
###############################################
###
###     Feedback is the users way of connecting 
###     with app admins through the app.
###

from flask import Blueprint, render_template, session
from app.views import _helpers


feedback_blueprint = Blueprint('feedback', __name__)


################# FEEDBACK FORM ##################

@feedback_blueprint.route('/feedback_page')
def feedback_page():
    try:
        return render_template('account/feedback.html', skeleton=_helpers.get_skeleton(),
        industry_slider='home/_industry_slider.html' if 'user_email' in session else None)
    except:
        return render_template('errors/500.html')