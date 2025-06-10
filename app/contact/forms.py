from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, Email, Length, Optional

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])

    # New fields
    phone_country_code = SelectField('Country Code', choices=[
        ('+1', '+1 (US)'),
        ('+91', '+91 (India)'),
        ('+44', '+44 (UK)'),
        ('+61', '+61 (Australia)'),
        ('+971', '+971 (UAE)')
    ], validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    state = StringField('State', validators=[Optional(), Length(max=100)]) # Made optional
    specialties = StringField('Specialties', validators=[Optional(), Length(max=200)]) # Made optional
    monthly_insurance = DecimalField('Monthly Insurance', validators=[Optional()]) # Use DecimalField for currency
    preferred_appointment_date = DateField('Preferred Appointment Date', format='%Y-%m-%d', validators=[Optional()])
    preferred_time_slot = SelectField('Preferred Time Slot', choices=[
        ('9:00 AM', '9:00 AM'),
        ('10:00 AM', '10:00 AM'),
        ('11:00 AM', '11:00 AM'),
        ('12:00 PM', '12:00 PM'),
        ('1:00 PM', '1:00 PM'),
        ('2:00 PM', '2:00 PM'),
        ('3:00 PM', '3:00 PM'),
        ('4:00 PM', '4:00 PM')
    ], validators=[Optional()])

    subject = StringField('Subject (Requirements)', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')