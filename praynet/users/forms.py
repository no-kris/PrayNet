from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo
from praynet.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    """User registration form with validation"""
    username = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8, max=30,
                               message='Password must be between 8 and 30 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')
    cancel = SubmitField('Cancel')

    def validate_username(self, username):
        """Check if the username is already taken"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if the email is already registered"""
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')
        

class LoginForm(FlaskForm):
    """User login form with email and password fields."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    cancel = SubmitField('Cancel')

class EditProfileForm(FlaskForm):
    """Form for editing user profile information."""
    username = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email(message='Invalid email address')
    ])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Update')
    cancel = SubmitField('Cancel')

    def validate_username(self, username):
        """Check if the new username is already taken"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Check if the new email is already registered"""
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')
           
class RequestResetForm(FlaskForm):
    """Form to request a password reset via email."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    cancel = SubmitField('Cancel')

    def validate_email(self, email):
        """Check if the email exists in the database."""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    """Form to reset the user's password."""
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8, max=30,
                               message='Password must be between 8 and 30 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')

class DeleteAccountForm(FlaskForm):
    """Form to confirm account deletion."""
    submit = SubmitField('Delete Account')
    cancel = SubmitField('Cancel')