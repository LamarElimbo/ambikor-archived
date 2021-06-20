#########################################
############## COLLECTIONS ##############
#########################################
###
###     Collections are like music playlist. They
###     allow users to save similar
###     careers into meaningful groups
###

from flask import Blueprint, redirect, render_template, request, session, url_for
from random import choice
from .. import mongo
from app.views import _helpers

collections_blueprint = Blueprint('collections', __name__)


############## COLLECTIONS PAGES ################

@collections_blueprint.route('/article/<collection_title>')
def content(collection_title):
    try:
        admin = mongo.db.admin.find_one({"username": "admin_lamar"})
        content = [coll for coll in admin['colls'] if coll['url'] == collection_title][0]
        careers = [mongo.db.careers.find_one({'title': career}) for career in content['careers']]
        for career in careers:
            career['videos'] = career['videos'][choice([0,1])]
        content['careers'] = careers
        if len(content['notes']) == 0:
            content['careers'] = sorted(content['careers'], key=lambda k: k['title'])
        return render_template('career/_career_panels.html',
                               career_content='collections/content.html',
                               industry_slider='home/_industry_slider.html',
                               skeleton=_helpers.get_skeleton(),
                               content=content,
                               has_notes='true' if len(content['notes']) > 0 else 'false',
                               careers=careers)
    except:
        return render_template('errors/500.html')

@collections_blueprint.route('/bookmarks')
def bookmarks_page():
    try:
        skeleton = _helpers.get_skeleton()
        admin = mongo.db.admin.find_one({"username": "admin_lamar"})
        if 'admin_username' in session:
            return render_template('admin/coll_page.html',
                                   skeleton=skeleton,
                                   admin=admin,
                                   collections=sorted([coll for coll in admin['colls']], key=lambda k: k['title']))
        careers = [mongo.db.careers.find_one({'career_id': item}) for item in skeleton['user']['bookmarks']['careers']]
        if len(careers) > 0:
            for career in careers:
                career['videos'] = career['videos'][choice([0,1])]
        collections = [coll for coll in admin['colls'] if coll['url'] in skeleton['user']['bookmarks']['collections']]
        profiles = [mongo.db.users.find_one({'user_id': item}) for item in skeleton['user']['bookmarks']['profiles']]
        return render_template('collections/bookmarks.html',
                               skeleton=skeleton, 
                               careers=careers[:2], 
                               collections=collections[:2], 
                               industry_slider='home/_industry_slider.html' if 'user_email' in session else None,
                               profiles=profiles[:2]) 
    except: 
        return render_template('errors/500.html')
    

@collections_blueprint.route('/collections_archive')
def collections_archive():
    try:
        admin = mongo.db.admin.find_one({"username": "admin_lamar"})
        return render_template('collections/collections_archive.html',
                               skeleton=_helpers.get_skeleton(),
                               num_careers= mongo.db.careers.count(),
                               collections=sorted([coll for coll in admin['colls']], key=lambda k: k['title']))
    except:
        return render_template('errors/500.html')
    
############## BOOKMARKING DYNAMICS ##############

@collections_blueprint.route('/get_bookmarked_collections', methods=["POST"])
def get_bookmarked_collections():
    admin = mongo.db.admin.find_one({"username": "admin_lamar"})
    user = mongo.db.users.find_one({"email": session['user_email']})
    bookmarked_items = user['bookmarks'][request.form['bookmarked_coll']]
    if request.form['bookmarked_coll'] == 'careers':
        careers = [mongo.db.careers.find_one({'career_id': item}) for item in bookmarked_items]
        if len(careers) > 0:
            for career in careers:
                career['videos'] = career['videos'][choice([0,1])]
        return render_template('collections/_bookmarked_careers.html', skeleton=_helpers.get_skeleton(), careers=careers)
    elif request.form['bookmarked_coll'] == 'collections':
        return render_template('collections/_bookmarked_collections.html', 
                               skeleton=_helpers.get_skeleton(),
                               collections=[coll for coll in admin['colls'] if coll['url'] in bookmarked_items])
    elif request.form['bookmarked_coll'] == 'profiles':
        return render_template('collections/_bookmarked_profiles.html', 
                               skeleton=_helpers.get_skeleton(),
                               profiles=[mongo.db.users.find_one({'user_id': item}) for item in bookmarked_items])
    return redirect(url_for('home.home_page'))

@collections_blueprint.route('/add_bookmark', methods=["POST"])
def add_bookmark():
    bookmark = request.form['bookmark'].split('-', 1)
    if bookmark[0] == 'career':
        mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$addToSet": {"bookmarks.careers": bookmark[1]}})
    elif bookmark[0] == 'collection':
        mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$addToSet": {"bookmarks.collections": bookmark[1]}})
    elif bookmark[0] == 'profile':
        mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$addToSet": {"bookmarks.profiles": bookmark[1]}})
    return redirect(url_for('home.home_page'))

@collections_blueprint.route('/remove_bookmark', methods=["POST"])
def remove_bookmark():
    bookmark = request.form['bookmark'].split('-', 1)
    if bookmark[0] == 'career':
        mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$pull": {"bookmarks.careers": bookmark[1]}})
    elif bookmark[0] == 'collection':
        mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$pull": {"bookmarks.collections": bookmark[1]}})
    elif bookmark[0] == 'profile':
        mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$pull": {"bookmarks.profiles": bookmark[1]}})
    return redirect(url_for('home.home_page'))