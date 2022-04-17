from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


from flask_learning.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.user_login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_learning.users.routes import users
    from flask_learning.posts.routes import posts
    from flask_learning.main.routes import main
    from flask_learning.errors.handlers import errors
    from flask_learning.flask_sijax.routes import flask_sijax

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(flask_sijax)

    return app

