from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_moment import Moment
from praynet.config import Config
import cloudinary

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
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

    cloudinary.config(
        cloud_name=app.config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=app.config.get('CLOUDINARY_API_KEY'),
        api_secret=app.config.get('CLOUDINARY_API_SECRET')
    )

    from praynet.models import User
    with app.app_context():
        db.create_all()

    from praynet.main.routes import main
    from praynet.users.routes import users
    from praynet.prayerposts.routes import prayerposts

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(prayerposts)

    return app