# Import flask and template operators
from config import app_config
from flask import Flask, render_template
from flask_pymongo import PyMongo
import os

app = Flask(__name__, instance_relative_config=True)

#config_type = 'development'
config_type = 'production'

app.config.from_object(app_config[config_type])
app.config.from_pyfile('config.py')

mongo = PyMongo(app)

#All the routings in our app will be mentioned here.
@app.route('/test')
def test():
    return "App is working perfectly"
    
from app.views.auth import auth_blueprint
from app.views.career import career_blueprint
from app.views.collections import collections_blueprint
from app.views.feedback import feedback_blueprint
from app.views.home import home_blueprint
from app.views.profile import profile_blueprint

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(career_blueprint)
app.register_blueprint(collections_blueprint)
app.register_blueprint(feedback_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(profile_blueprint)

# Error handling
def page_not_found(e):
    return render_template('errors/404.html'), 404
app.register_error_handler(404, page_not_found)

def forbidden(e):
    return render_template('errors/403.html'), 403
app.register_error_handler(403, forbidden)

def internal_server_error(e):
    return render_template('errors/500.html'), 500
app.register_error_handler(500, internal_server_error)


# How to export new database from mac to mLab
# Connect to mongodb with: mongod
# Create bson file of database with: mongodump --db clustrComp --collection companies
# Upload file and replace old database with: mongorestore -h ds111063.mlab.com:11063 -d heroku_66k3xx0k -c companies -u heroku_66k3xx0k -p 5j3c5kg20obnho0h8n1usdqiad dump/clustrComp/companies.bson

# How to import new database from mLab to mac
#mongodump -h ds111063.mlab.com:11063 -d heroku_66k3xx0k -c admin -u heroku_66k3xx0k -p 5j3c5kg20obnho0h8n1usdqiad
#mongorestore -d clustrComp -c admin --drop dump/heroku_66k3xx0k/admin.bson