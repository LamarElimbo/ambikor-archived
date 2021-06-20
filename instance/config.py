import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ambicore'
    #SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2016@localhost/dreamteam_db'