from datetime import datetime
from flask import current_app, url_for
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import Table
from praynet import login_manager, db
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

friends = db.Table(
    'friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    """User model for storing user information."""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    prayer_requests = db.relationship('PrayerRequest', backref='author', lazy=True)
    prayer_offers = db.relationship('PrayerOffer', backref='responder', lazy=True)
    friends = db.relationship(
        'User', secondary=friends,
        primaryjoin=(friends.c.user_id == id),
        secondaryjoin=(friends.c.friend_id == id),
        backref=db.backref('friend_of', lazy='dynamic'),
        lazy='dynamic'
    )

    def get_reset_token(self, expires_seconds=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)
    
    @property
    def profile_image_url(self):
        """Return the user's profile picture URL, or default if not set."""
        if self.image_file:
            return self.image_file
        else:
            return url_for('static', filename='images/profile_pics/default.png')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    
class PrayerRequest(db.Model):
    """Model for storing prayer requests."""
    __tablename__ = 'prayer_request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='General')
    offers = db.relationship('PrayerOffer', backref='prayer_request', lazy=True)

    def __repr__(self):
        return f"PrayerRequest('{self.title}', '{self.date_posted}')"
    
class PrayerOffer(db.Model):
    """Model for storing prayer offers."""
    __tablename__ = 'prayer_offer'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prayer_request_id = db.Column(db.Integer, db.ForeignKey('prayer_request.id'), nullable=False)

    def __repr__(self):
        return f"PrayerOffer('{self.date_posted}')"
