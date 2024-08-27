#import os
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import config_dev as config

bootstrap = Bootstrap5()
mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Some safe defaults for the (development) server to use
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI= 'sqlite:///app.db',
        SECURITY_PASSWORD_SALT ="very-important"
    )

    if test_config == 'testing':
        app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        LP_ADMIN='administrator@example.com',
        TESTING = True ) 
    else:
        app.config.from_object(config.Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .groups import groups as groups_blueprint
    app.register_blueprint(groups_blueprint, url_prefix='/groups')

    from .manage import manage as manage_blueprint
    app.register_blueprint(manage_blueprint, url_prefix='/manage')

    return app
