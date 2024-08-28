# These are specimen configuration values. You should change them all for values appropriate to you.
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    LP_GROUP_NAME="Brian's Groups"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="BrianButcher",
    password="Romanticism",
    hostname="BrianButcher.mysql.eu.pythonanywhere-services.com",
    databasename="BrianButcher$Bergama",)
    SQLALCHEMY_ENGINE_OPTIONS= {'pool_recycle' : 280}
    SECRET_KEY = 'top secret'
    LP_ADMIN = 'administrator_email@example.com'
    DEFAULT_GROUP_NAME = 'Phil'

    # Mail Globals appropriate to my philosopy group
    MAIL_DEFAULT_SENDER='my email address'
    LP_MAIL_SUBJECT_PREFIX='[Philosophy Group Name]'
    LP_MAIL_SENDER =' <admistrator@my.philosophy.group>' 

    # Gmail configuration globals
    MAIL_USERNAME='me@gmail.com'
    MAIL_PASSWORD='google allocated password'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @staticmethod
    def init_app(app):
        pass

