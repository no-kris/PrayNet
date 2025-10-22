from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from praynet import db
from praynet.models import PrayerOffer, PrayerRequest, User
from praynet.prayerposts.forms import PrayerRequestForm


prayerposts = Blueprint('prayerposts', __name__, template_folder='../templates/prayerposts')

@prayerposts.route('/prayer_requests/<string:username>')
@login_required
def user_prayer_requests(username):
    """Display all the current users prayer requests."""
    if username != current_user.username:
        abort(403)
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    prayer_requests = (PrayerRequest.query
                       .filter_by(author=user)
                       .order_by(PrayerRequest.date_posted.desc())
                       .paginate(page=page, per_page=5))
    return render_template('user_prayer_requests.html', 
                         requests=prayer_requests,
                         user=user,
                         page=page)

@prayerposts.route('/request/new', methods=['GET', 'POST'])
@login_required
def create_new_request():
    """
    Allow authenticated users to create new prayer requests.
    """
    form = PrayerRequestForm()
    if request.method == 'POST':
        if form.cancel.data:
            return redirect(url_for('prayerposts.user_prayer_requests', username=current_user.username))
        if form.validate_on_submit():
            prayer_request = PrayerRequest(
                title=form.title.data,
                content=form.content.data,
                category=form.category.data,
                user_id=current_user.id
            )
            db.session.add(prayer_request)
            db.session.commit()
            flash('Your prayer request has been shared.', 'success')
            return redirect(url_for('prayerposts.user_prayer_requests', username=current_user.username))
    return render_template('create_prayer_request.html', 
                           title='New Prayer Request', 
                           form=form, 
                           legend='Share Prayer Request')

@prayerposts.route('/prayer_requests/<int:post_id>')
def prayer_requests(post_id):
    """
    Display single prayer request using the id for that request.
    """
    prayer_request = PrayerRequest.query.get_or_404(post_id)
    prayer_offers = PrayerOffer.query.filter_by(prayer_request_id=post_id).order_by(PrayerOffer.date_posted.asc()).all()
    return render_template('prayer_request.html', 
                           title=prayer_request.title, 
                           request=prayer_request,
                           prayers=prayer_offers)


@prayerposts.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_request(post_id):
    """
    Delete the users specific prayer request.
    """
    prayer_request = PrayerRequest.query.get_or_404(post_id)
    if prayer_request.author != current_user:
        abort(403)
    db.session.delete(prayer_request)
    db.session.commit()
    flash('Post has been successfully deleted', 'success')
    return redirect(url_for('prayerposts.user_prayer_requests', username=current_user.username))

@prayerposts.route('/offer_prayer/<int:post_id>', methods=['POST'])
def offer_prayer(post_id):
    """
    Insert a prayer into the specific prayer request.
    """
    content = request.form['content']
    prayer_offer = PrayerOffer(
        content=content,
        user_id=current_user.id,
        prayer_request_id=post_id
    )
    db.session.add(prayer_offer)
    db.session.commit()
    return redirect(url_for('prayerposts.prayer_requests', post_id=post_id))

@prayerposts.route('/offer_prayers')
def offer_prayers():
    """
    Page to search for users by username and display their prayer requests.
    """
    query = request.args.get('q', '')
    users = []

    if query:
        users = User.query.filter(User.username.ilike(f"%{query}%")).all()

    for user in users:
        user.requests = PrayerRequest.query.filter_by(author=user).order_by(PrayerRequest.date_posted.desc()).all()

    return render_template('offer_prayers.html', users=users, query=query)

