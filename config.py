# config.py

import os

###############################
######## Configure App ########
###############################

class Config(object):
    """ Common configurations """
    SECRET_KEY = "ambicore"
    TESTING = False

    
class DevelopmentConfig(Config): # Heroku off
    """ Development configurations """
    MONGO_URI = "mongodb+srv://heroku_66k3xx0k:5j3c5kg20obnho0h8n1usdqiad@cluster-66k3xx0k.jjm6y.mongodb.net/heroku_66k3xx0k?retryWrites=true&w=majority"
    DEBUG = True
    TESTING = False
    MONGO_DBNAME = 'heroku_66k3xx0k'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    
class ProductionConfig(Config): # Heroku on
    """ Production configurations """
    DEBUG = False
    TESTING = True
    try:
        MONGO_URI = "mongodb+srv://heroku_66k3xx0k:5j3c5kg20obnho0h8n1usdqiad@cluster-66k3xx0k.jjm6y.mongodb.net/heroku_66k3xx0k?retryWrites=true&w=majority"
        MONGO_DBNAME = 'ambikor'
        BROKER_URL = os.environ['REDIS_URL']
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    except:
        print('running local configuration')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}