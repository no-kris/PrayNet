from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class PrayerRequestForm(FlaskForm):
    """
    Form for creating prayer requests.
    """
    title = StringField('Title', validators=[
        DataRequired()
    ])
    content = TextAreaField('content', validators=[
        DataRequired()
    ])
    category = SelectField(
        'Category',
        validators=[DataRequired()],
        choices=[
            ('General', 'General'),
            ('Healing', 'Healing'),
            ('Guidance', 'Guidance'),
            ('Thanksgiving', 'Thanksgiving'),
            ('Family', 'Family'),
            ('Financial', 'Financial'),
            ('Relationships', 'Relationships'),
            ('Spiritual Growth', 'Spiritual Growth'),
            ('Protection', 'Protection'),
        ]
    )
    submit = SubmitField('Share Request')
    cancel = SubmitField('Cancel')

class PrayerOfferForm(FlaskForm):
    """
    Form for creating prayer offers.
    """
    content = TextAreaField('Your Prayer (optional)')
    submit = SubmitField('Offer Prayer')
    cancel = SubmitField('Cancel')