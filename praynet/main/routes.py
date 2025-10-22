from flask import Blueprint, render_template, request
from datetime import date, datetime, timedelta
from .dailyverses import verses
import requests
from praynet.models import PrayerRequest

main = Blueprint('main', __name__)

daily_verse = None
last_update_date = None

def get_daily_verse():
    global daily_verse, last_update_date
    
    today = date.today()
    if daily_verse is None or last_update_date != today:
        today_index = today.toordinal() % len(verses)
        verse_ref = verses[today_index]
        response = requests.get(f"https://bible-api.com/{verse_ref}")
        verse_data = response.json()
        daily_verse = f'{verse_data["text"]} - {verse_data["reference"]}'
        last_update_date = today
    
    return daily_verse

def get_trending_prayers(days=7):
    """
    Retrieve the 5 most recent trending prayer requests posted within the last `days` days.

    Args:
        days (int, optional): The number of past days to consider for trending prayers. 
                              Defaults to 7.

    Returns:
        list[PrayerRequest]: A list of up to 5 PrayerRequest objects, 
                             ordered from newest to oldest.
    """
    time_delta = datetime.now() - timedelta(days)
    return (PrayerRequest.query
                .filter(PrayerRequest.date_posted >= time_delta)
                .order_by(PrayerRequest.date_posted.desc())
                .limit(5)
                .all())

@main.route('/')
@main.route('/home')
def home():
    """
    Home page displaying paginated prayer request posts with category filter.
    """
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')

    if category == 'all':
        query = PrayerRequest.query.order_by(PrayerRequest.date_posted.desc())
    else:
        query = PrayerRequest.query.filter_by(category=category).order_by(PrayerRequest.date_posted.desc())

    paginated_page = query.paginate(page=page, per_page=3)
    
    trending = get_trending_prayers(days=7)

    daily_verse = get_daily_verse()
    
    return render_template(
        'base.html',
        requests=paginated_page,
        category=category,
        trending=trending,
        daily_verse=daily_verse
    )


@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/community_guidelines')
def community_guidelines():
    return render_template('community-guidelines.html', title='Community Guidelines')

