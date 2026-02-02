from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from praynet.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from praynet.models import (  # Import models so SQLAlchemy knows about them
        PrayerOffer,
        PrayerRequest,
        User,
    )

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            import sys

            print(f"Error creating database tables: {e}", file=sys.stderr)

    from praynet.main.routes import main
    from praynet.prayerposts.routes import prayerposts
    from praynet.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(prayerposts)

    return app
