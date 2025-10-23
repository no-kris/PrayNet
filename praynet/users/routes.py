from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from praynet.users.forms import DeleteAccountForm, EditProfileForm, RegistrationForm, LoginForm, RequestResetForm
from praynet import db, bcrypt
from praynet.models import User
from praynet.users.utils import save_picture_cloudinary, send_reset_email

users = Blueprint('users', __name__, template_folder='../templates/profiles')

@users.route('/profile')
@login_required
def profile():
    try:
        flash('Loading profile...', 'info')
    except Exception as e:
        print(f"Flash error: {e}")
    return render_template('profile.html', current_user=current_user)

@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Registration page with form handling.
    If the form is submitted and valid, redirect to home page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if request.method == "POST":
        if form.cancel.data:
            return redirect(url_for('main.home'))
        if form.validate_on_submit():
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page with form handling.
    If the form is submitted and valid, redirect to home page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.cancel.data:
            return redirect(url_for('main.home'))
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    """Logout the current user and redirect to home page."""
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Update user profile information."""
    form = EditProfileForm()
    if request.method == "POST":
        if form.cancel.data:
            return redirect(url_for('users.profile'))
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            if form.picture.data:
                picture_url = save_picture_cloudinary(form.picture.data)
                print(picture_url) 
                current_user.image_file = picture_url
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.profile'))
    else:
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@users.route("/change_password_request", methods=["GET", "POST"])
@login_required
def change_password_request():
    """Route for displaying requests to change password for currently logged in users."""
    form = RequestResetForm()
    if form.cancel.data:
        return redirect(url_for('users.profile'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('change_password_request.html', title='Reset Password', form=form)

@users.route("/forgot_password", methods=["GET", "POST"])
def forgot_password_request():
    """Route for changing password when the user has forgotten it.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.cancel.data:
        return redirect(url_for('users.profile'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('change_password_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """Route for resetting password using a token."""
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.change_password_request'))
    form = RequestResetForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password_token.html', title='Reset Password', form=form)

@users.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    """Delete the current user's account."""
    user = User.query.get(current_user.id)
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted.', 'info')
    return redirect(url_for('main.home'))

@users.route("/delete-account-confirm", methods=["GET", "POST"])
@login_required
def delete_account_confirm():
    """Render a confirmation page before deleting the account."""
    form = DeleteAccountForm()
    if request.method == "POST":
        if form.submit.data:
            return redirect(url_for('users.delete_account'))
        else:
            return redirect(url_for('users.profile'))
    return render_template('delete_account_confirm.html', title='Delete Account', form=form)