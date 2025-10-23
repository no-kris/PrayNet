from io import BytesIO
from PIL import Image
import cloudinary.uploader
from praynet import mail
from flask import current_app, url_for
from flask_mail import Message


def send_reset_email(user):
    """Helper function to send a password reset email to the user."""
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='kris.tresk@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



