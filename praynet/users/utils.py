from io import BytesIO
from PIL import Image
import cloudinary.uploader
from praynet import mail
from flask import current_app, url_for
from flask_mail import Message

def save_picture_cloudinary(form_picture):
    """
    Uploads user's profile image to Cloudinary.
    Returns the secure URL to save in the database.
    """
    try:
        img = Image.open(form_picture)
        img.thumbnail((125, 125))

        img_bytes = BytesIO()
        img_format = img.format if img.format else 'PNG'
        img_format = img_format.upper()
        if img_format == 'JPG':
            img_format = 'JPEG'

        img.save(img_bytes, format=img_format)
        img_bytes.seek(0)

        result = cloudinary.uploader.upload(img_bytes, folder="profile_pics")
        return result["secure_url"]

    except Exception as e:
        current_app.logger.error(f"Cloudinary upload failed: {e}")
        raise

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



