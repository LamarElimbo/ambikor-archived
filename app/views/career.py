##############################################
################## CAREERS ###################
##############################################

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from .. import mongo
from app.views import _helpers
import datetime, os, uuid
from random import shuffle

career_blueprint = Blueprint('career', __name__)

################# CAREER PAGES ##################
    
@career_blueprint.route('/career_title/<career_title>', methods=['GET', 'POST'])
def career_page_title(career_title):
    try:
        career = mongo.db.careers.find_one({'title': career_title})
        return redirect(url_for('career.career_page', career_id=career['career_id']))
    except:
        return render_template('errors/500.html')

@career_blueprint.route('/career/<career_id>', methods=['GET', 'POST'])
def career_page(career_id):
    try:
        if request.method == 'POST':
            mongo.db.careers.find_one_and_update({'career_id': career_id}, {"$set": {'title': request.form['title'].lower(), 'alternative_titles': request.form['alternative_titles'].lower().split(', '), 'description': request.form['description'], 'image': request.form['image'], 'videos': [video.replace('watch?v=','embed/') for video in request.form['videos'].split(',')], 'tags': request.form['tags'].split(','), "services": {"suggestions": []}}})
        career = mongo.db.careers.find_one({'career_id': career_id})
        try:
            users = [mongo.db.users.find_one({"user_id": user}) for user in career['users']]
        except:
            users = []
        return render_template('admin/career_admin.html' if 'admin_username' in session else 'career/career.html',
                               career_page='true',
                               skeleton=_helpers.get_skeleton(),
                               industry_slider='home/_industry_slider.html',
                               admin=mongo.db.admin.find_one({'username': 'admin_lamar'}),
                               message='none',
                               action='update' if 'admin_username' in session else 'None',
                               num_careers= mongo.db.careers.count(),
                               career=career,
                               users=[user for user in users if len(user['profile']['services']) > 0],
                               careers_list=[{'id': career['career_id'], 'title': career['title']} for career in mongo.db.careers.find().sort('title')])
    except:
        return render_template('errors/500.html')

@career_blueprint.route('/careers/<career_cats>')
def career_search(career_cats):
    try:
        admin = mongo.db.admin.find_one({"username": "admin_lamar"})
        collections = [coll for coll in admin['colls'] if career_cats in coll['tags'] and coll['action'] == 'publish']
        shuffle(collections)
        cats = [cat.replace('sportsrec', 'sports-rec') for cat in career_cats.split('+')]
        query_meld = ', '.join(cats)
        careers = mongo.db.careers.find({'tags': { '$all': cats}}).sort("title")
        return render_template('career/career_search_results.html',
                               skeleton=_helpers.get_skeleton(),
                               industry_slider='home/_industry_slider.html',
                               collections=collections,
                               category=career_cats,
                               query=' + '.join(query_meld.rsplit(', ', 1)),
                               num_careers=careers.count(),
                               careers=[career for career in careers])
    except:
        return render_template('errors/500.html')

@career_blueprint.route('/careers')
def career_archive():
    try:
        admin = mongo.db.admin.find_one({"username": "admin_lamar"})
        collections = [coll for coll in admin['colls'] if coll['action'] == 'publish']
        shuffle(collections)
        return render_template('career/career_archive.html',
                               skeleton=_helpers.get_skeleton(),
                               industry_slider='home/_industry_slider.html',
                               num_careers= mongo.db.careers.count(),
                               collections=collections,
                               careers=[career for career in mongo.db.careers.find().sort('title') if career['title'][0] == 'a'])
    except:
        return render_template('errors/500.html')
    
@career_blueprint.route('/careers/index/<letter>')
def get_careers_index(letter):
    try:
        return render_template('career/career_search_results.html',
                               skeleton=_helpers.get_skeleton(),
                               industry_slider='home/_industry_slider.html',
                               careers=[career for career in mongo.db.careers.find().sort("title") if career['title'][0] == letter])
    except:
        return render_template('errors/500.html')

@career_blueprint.route('/bookmark_career', methods=['POST'])
def bookmark_career():
    if 'user_email' in session:
        if request.form["action"] == 'bookmark':
            mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$addToSet": {"careers.saved": request.form['career_id']}})
        else:
            mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$pull": {"careers.saved": request.form['career_id']}})
    return redirect(url_for('career.career_archive'))

@career_blueprint.route('/delete_career', methods=['POST'])
def delete_career():
    if 'admin_username' in session:
        flash("You successfully removed a career.")
        mongo.db.careers.remove({"career_id": request.form["id"]})
    return redirect(url_for('career.career_archive'))