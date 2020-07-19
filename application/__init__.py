from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.config import Config
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'home.login'
    login_manager.init_app(app)

    from application.model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from application.home.routes import home
    from application.user.routes import user
    app.register_blueprint(home)
    app.register_blueprint(user)

    return app
