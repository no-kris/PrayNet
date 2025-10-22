import os
import secrets
from PIL import Image
from flask_login import current_user
from praynet import mail
from flask import current_app, url_for
from flask_mail import Message

def save_picture(form_picture):
    """Helper function to save users uploaded image to file system."""
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/profile_pics', picture_fn)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_fn

def remove_old_image():
    if current_user.image_file != 'default.png':
        old_path = os.path.join(
            current_app.root_path,
            'static/images/profile_pics',
            current_user.image_file
        )
        try:
            if os.path.exists(old_path):
                os.remove(old_path)
        except Exception as e:
            current_app.logger.warning(f"Could not remove old profile image: {e}")

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



