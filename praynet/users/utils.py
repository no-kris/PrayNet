from io import BytesIO
from PIL import Image
import cloudinary
from praynet import mail
from flask import url_for
from flask_mail import Message

def save_picture_cloudinary(form_picture):
    """
    Uploads user's profile image to Cloudinary.
    Returns the secure URL to save in the database.
    """
    img = Image.open(form_picture)
    output_size = (125, 125)
    img.thumbnail(output_size)

    # Save to in-memory file
    img_bytes = BytesIO()
    img.save(img_bytes, format=img.format)
    img_bytes.seek(0)

    result = cloudinary.uploader.upload(img_bytes, folder="profile_pics")
    return result["secure_url"]

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



