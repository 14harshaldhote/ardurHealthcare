from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError

def validate_specialties(form, field):
    """Custom validator for specialties field - ensures at least one specialty is selected"""
    # Handle both empty and whitespace-only values
    if not field.data or not field.data.strip():
        raise ValidationError('Please select at least one specialty.')

    # Additional validation: check if the data contains actual specialty names
    # (not just whitespace or commas)
    specialties_list = [s.strip() for s in field.data.split(',') if s.strip()]
    if not specialties_list:
        raise ValidationError('Please select at least one specialty.')

    # Validate each specialty is not empty and has reasonable length
    for specialty in specialties_list:
        if len(specialty) < 2:
            raise ValidationError('Each specialty must be at least 2 characters long.')
        if len(specialty) > 100:
            raise ValidationError('Each specialty must be less than 100 characters.')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Name is required.'), Length(max=100, message='Name must be less than 100 characters.')])
    email = StringField('Email', validators=[DataRequired(message='Email is required.'), Email(message='Please enter a valid email address.'), Length(max=120, message='Email must be less than 120 characters.')])

    # Enhanced fields for state page form
    phone_country_code = SelectField('Country Code', choices=[
        ('+1', '+1 (US)'),
        ('+91', '+91 (India)'),
        ('+44', '+44 (UK)'),
        ('+61', '+61 (Australia)'),
        ('+971', '+971 (UAE)'),
        ('+33', '+33 (France)'),
        ('+49', '+49 (Germany)'),
        ('+81', '+81 (Japan)'),
        ('+86', '+86 (China)'),
        ('+55', '+55 (Brazil)')
    ], validators=[Optional()], default='+1')
    phone_number = StringField('Phone Number', validators=[DataRequired(message='Phone number is required.'), Length(min=10, max=20, message='Phone number must be between 10-20 characters.')])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])  # Alternative phone field for state pages
    practice = StringField('Practice Name', validators=[DataRequired(message='Practice name is required.'), Length(max=200, message='Practice name must be less than 200 characters.')])
    state = StringField('State', validators=[DataRequired(message='State is required.'), Length(max=100, message='State must be less than 100 characters.')])

    # Changed from SelectMultipleField to StringField - custom validation for JavaScript handling
    specialties = StringField('Specialties', validators=[validate_specialties, Length(max=500, message='Specialties list is too long.')])

    # Service type field
    service_type = SelectField('Service Type', choices=[
        ('', 'Select service type'),
        ('medical-billing', 'Medical Billing'),
        ('coding-services', 'Coding Services'),
        ('credentialing', 'Provider Credentialing'),
        ('ar-management', 'AR Management'),
        ('denial-management', 'Denial Management'),
        ('full-service', 'Full Service Package'),
        ('consultation', 'Consultation')
    ], validators=[DataRequired(message='Please select a service type.')])

    # Optional fields for detailed contact form
    monthly_insurance = DecimalField('Monthly Insurance Collections ($)', validators=[Optional()], places=2)
    preferred_appointment_date = DateField('Preferred Appointment Date', format='%Y-%m-%d', validators=[Optional()])
    preferred_time_slot = SelectField('Preferred Time Slot', choices=[
        ('', 'Select preferred time'),
        ('9:00 AM', '9:00 AM'),
        ('10:00 AM', '10:00 AM'),
        ('11:00 AM', '11:00 AM'),
        ('12:00 PM', '12:00 PM'),
        ('1:00 PM', '1:00 PM'),
        ('2:00 PM', '2:00 PM'),
        ('3:00 PM', '3:00 PM'),
        ('4:00 PM', '4:00 PM')
    ], validators=[Optional()])

    subject = StringField('Subject (Requirements)', validators=[Optional(), Length(max=200, message='Subject must be less than 200 characters.')])
    message = TextAreaField('Message', validators=[DataRequired(message='Message is required.'), Length(min=10, max=1000, message='Message must be between 10-1000 characters.')])
    privacy_policy_agreement = BooleanField('I agree to the Privacy Policy', validators=[DataRequired(message='You must agree to the Privacy Policy to proceed.')])
    submit = SubmitField('Send Message')

    def validate_phone_number(self, field):
        """Custom validation for phone number format"""
        import re
        phone = field.data.strip() if field.data else ''

        # Remove common formatting characters
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)

        # Check if it contains only digits after cleaning
        if not clean_phone.isdigit():
            raise ValidationError('Phone number must contain only digits, spaces, hyphens, and parentheses.')

        # Check minimum length (adjust as needed)
        if len(clean_phone) < 10:
            raise ValidationError('Phone number must be at least 10 digits.')
