#################################################
################## HOME PAGES ###################
#################################################

from flask import Blueprint, render_template, session
from .. import mongo
from app.views import _helpers
from random import choice, shuffle
import collections


home_blueprint = Blueprint('home', __name__)
    
@home_blueprint.route('/career_guide_info')
def career_guide_info():
    try:
        return render_template('general/career_guide_info.html',
         industry_slider='home/_industry_slider.html' if 'user_email' in session else None,
         skeleton=_helpers.get_skeleton())
    except:
        return render_template('errors/500.html')

@home_blueprint.route('/money_info')
def money_info():
    try:
        return render_template('general/money_info.html',
        industry_slider='home/_industry_slider.html' if 'user_email' in session else None,
        skeleton=_helpers.get_skeleton())
    except:
        return render_template('errors/500.html')

@home_blueprint.route('/about')
def about():
    try:
        return render_template('general/about.html',
        industry_slider='home/_industry_slider.html' if 'user_email' in session else None,
        skeleton=_helpers.get_skeleton())
    except:
        return render_template('errors/500.html')
        
@home_blueprint.route('/')
def home_page():
        admin = mongo.db.admin.find_one({"username": "admin_lamar"})
        career_content = [career for career in mongo.db.careers.find()]
        shuffle(career_content)
        for content in career_content:
            content['videos'] = content['videos'][choice([0,1])]
        collections = [coll for coll in admin['colls'] if coll['action'] == 'publish']
        shuffle(collections)
        sample_services = [
            {'name':'Willy Wonka', 'img':'../../../static/images/sample_services/wonka.png', 'career':'Confectioner (Candy Maker)', 'service':'Candy Critique', 'cost':'25', 'description':"Good morning Starshine, the earth says hello! Come visit my factory (no golden ticket necessary) and show me some of your sweet creations. I'll give you my honest review and have you leaving with some quality constructive feedback."},
            {'name':'Cristina Yang', 'img':'../../../static/images/sample_services/yang.png', 'career':'Cardiothoracic Surgeon', 'service':'Shadow Shift', 'cost':'175', 'description':"Have some fire, be unstoppable, be a force of nature, and be prepeared to learn. It's a selective process, but I'm allowing a chosen few to shadow me in my hospital for a day."},
            {'name':'Mrs. Doubtfire', 'img':'../../../static/images/sample_services/doubtfire.png', 'career':'Voice Over Actor', 'service':'Phone Chat', 'cost':'5', 'description':"Hello dearie, I am Euphegenia Doubtfire and I would like to offer you the chance to have a phone call with me and get some feedback on your voice acting."},
            {'name':'Miranda Preastly', 'img':'../../../static/images/sample_services/preastly.png', 'career':'Magazine Editor', 'service':'Guest Lecture', 'cost':'200', 'description':"I've been feeling an unprecedented urge to give back, so now is your chance to have me as a guest lecturer and learn from the many insights i've garnered about fashion throughout my esteemed career."},
            {'name':'Katniss Everdeen', 'img':'../../../static/images/sample_services/katniss.png', 'career':'Archer', 'service':'Technique Critique', 'cost':'15', 'description':"Good form, accuracy, and precision are going to be your best friends and I'm here to make sure they're at your disposal. So send me a video of you practicing archery and I'll tell you how to improve."},
            {'name':'Rocky', 'img':'../../../static/images/sample_services/rocky.png', 'career':'Boxer', 'service':'Train With Me', 'cost':'80', 'description':"It ain't about how hard you hit. It's about how hard you can get hit and keep moving forward. Get in the ring with me and I'll teach you how to improve your resilience."},
            {'name':'Elle Woods', 'img':'../../../static/images/sample_services/elle.png', 'career':'Lawyer', 'service':'Application Prep', 'cost':'50', 'description':"So you wanna go to Harvard? You can totally do it! Trust me, it's not like it's hard, but if you want a helping hand in preparing your application, I'm definitely your girl!"},
            {'name':'Patrick Bateman', 'img':'../../../static/images/sample_services/psycho.png', 'career':'Investment Banker', 'service':'Business Card Redesign', 'cost':"30", 'description':"It's a known fact that I have the highest quality taste in business cards and I'm willing to help you class up yours."}
        ]
        shuffle(sample_services)
        return render_template('career/_career_panels.html',
                               career_content='home/home.html',
                               industry_slider='home/_industry_slider.html' if 'user_email' in session else None,
                               skeleton=_helpers.get_skeleton(),
                               collections=collections,
                               sample_services=sample_services)
    

############## CONTENT DYNAMICS ##############

@home_blueprint.route('/open_career_search_form')
def open_career_search_form():
    return render_template('career/_career_search_form.html',
                           careers_list=[{'id': career['career_id'], 'title': career['title']} for career in mongo.db.careers.find().sort('title')])