from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, IntegerField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange
from .models import LeadStatus, ClientStatus, ServiceType, Priority

class LeadForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    website = StringField('Website', validators=[Optional(), Length(max=200)])
    specialty = SelectField('Medical Specialty', choices=[
        ('', 'Select Specialty'),
        ('mental_health', 'Mental Health'),
        ('behavioral_health', 'Behavioral Health'),
        ('clinical_psychology', 'Clinical Psychology'),
        ('family_medicine', 'Family Medicine'),
        ('internal_medicine', 'Internal Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('orthopedics', 'Orthopedics'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('gastroenterology', 'Gastroenterology'),
        ('pulmonology', 'Pulmonology'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('anesthesiology', 'Anesthesiology'),
        ('radiology', 'Radiology'),
        ('pathology', 'Pathology'),
        ('ophthalmology', 'Ophthalmology'),
        ('otolaryngology', 'ENT'),
        ('urology', 'Urology'),
        ('obstetrics_gynecology', 'OB/GYN'),
        ('surgery', 'General Surgery'),
        ('plastic_surgery', 'Plastic Surgery'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    services_interested = SelectMultipleField('Services Interested', choices=[
        ('medical_billing', 'Medical Billing Services'),
        ('eligibility_verification', 'Eligibility & Benefits Verification'),
        ('prior_authorization', 'Prior Authorization Services'),
        ('provider_credentialing', 'Provider Credentialing & Enrollment'),
        ('charge_entry', 'Charge Entry Services'),
        ('medical_coding', 'Medical Coding Services'),
        ('claim_submission', 'Claim Submission & Follow-up'),
        ('payment_posting', 'Payment Posting & Reconciliation'),
        ('denial_management', 'Denial Management Services'),
        ('ar_management', 'Accounts Receivable Management'),
        ('full_rcm', 'Full Revenue Cycle Management')
    ])
    
    status = SelectField('Status', choices=[
        (LeadStatus.NEW.value, 'New'),
        (LeadStatus.CONTACTED.value, 'Contacted'),
        (LeadStatus.QUALIFIED.value, 'Qualified'),
        (LeadStatus.PROPOSAL_SENT.value, 'Proposal Sent'),
        (LeadStatus.NEGOTIATION.value, 'Negotiation'),
        (LeadStatus.CLOSED_WON.value, 'Closed Won'),
        (LeadStatus.CLOSED_LOST.value, 'Closed Lost'),
        (LeadStatus.ON_HOLD.value, 'On Hold')
    ], validators=[DataRequired()])
    
    priority = SelectField('Priority', choices=[
        (Priority.LOW.value, 'Low'),
        (Priority.MEDIUM.value, 'Medium'),
        (Priority.HIGH.value, 'High'),
        (Priority.URGENT.value, 'Urgent')
    ], validators=[DataRequired()])
    
    source = StringField('Lead Source', validators=[Optional(), Length(max=100)])
    assigned_to = StringField('Assigned To', validators=[Optional(), Length(max=50)])
    follow_up_date = DateField('Follow-up Date', validators=[Optional()])
    estimated_value = FloatField('Estimated Value ($)', validators=[Optional(), NumberRange(min=0)])
    probability = IntegerField('Probability (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Save Lead')

class ClientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    website = StringField('Website', validators=[Optional(), Length(max=200)])
    specialty = SelectField('Medical Specialty', choices=[
        ('', 'Select Specialty'),
        ('mental_health', 'Mental Health'),
        ('behavioral_health', 'Behavioral Health'),
        ('clinical_psychology', 'Clinical Psychology'),
        ('family_medicine', 'Family Medicine'),
        ('internal_medicine', 'Internal Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('orthopedics', 'Orthopedics'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('gastroenterology', 'Gastroenterology'),
        ('pulmonology', 'Pulmonology'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('anesthesiology', 'Anesthesiology'),
        ('radiology', 'Radiology'),
        ('pathology', 'Pathology'),
        ('ophthalmology', 'Ophthalmology'),
        ('otolaryngology', 'ENT'),
        ('urology', 'Urology'),
        ('obstetrics_gynecology', 'OB/GYN'),
        ('surgery', 'General Surgery'),
        ('plastic_surgery', 'Plastic Surgery'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    services = SelectMultipleField('Services Provided', choices=[
        ('medical_billing', 'Medical Billing Services'),
        ('eligibility_verification', 'Eligibility & Benefits Verification'),
        ('prior_authorization', 'Prior Authorization Services'),
        ('provider_credentialing', 'Provider Credentialing & Enrollment'),
        ('charge_entry', 'Charge Entry Services'),
        ('medical_coding', 'Medical Coding Services'),
        ('claim_submission', 'Claim Submission & Follow-up'),
        ('payment_posting', 'Payment Posting & Reconciliation'),
        ('denial_management', 'Denial Management Services'),
        ('ar_management', 'Accounts Receivable Management'),
        ('full_rcm', 'Full Revenue Cycle Management')
    ])
    
    status = SelectField('Status', choices=[
        (ClientStatus.ACTIVE.value, 'Active'),
        (ClientStatus.INACTIVE.value, 'Inactive'),
        (ClientStatus.SUSPENDED.value, 'Suspended'),
        (ClientStatus.TERMINATED.value, 'Terminated')
    ], validators=[DataRequired()])
    
    assigned_to = StringField('Account Manager', validators=[Optional(), Length(max=50)])
    contract_value = FloatField('Contract Value ($)', validators=[Optional(), NumberRange(min=0)])
    contract_start_date = DateField('Contract Start Date', validators=[Optional()])
    contract_end_date = DateField('Contract End Date', validators=[Optional()])
    
    billing_contact = StringField('Billing Contact', validators=[Optional(), Length(max=100)])
    billing_email = StringField('Billing Email', validators=[Optional(), Email()])
    billing_address = TextAreaField('Billing Address', validators=[Optional(), Length(max=300)])
    
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Save Client')

class ActivityForm(FlaskForm):
    type = SelectField('Activity Type', choices=[
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('task', 'Task'),
        ('note', 'Note')
    ], validators=[DataRequired()])
    
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    assigned_to = StringField('Assigned To', validators=[Optional(), Length(max=50)])
    
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    
    due_date = DateField('Due Date', validators=[Optional()])
    submit = SubmitField('Save Activity')

class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[Optional()])
    search_type = SelectField('Search In', choices=[
        ('all', 'All Fields'),
        ('name', 'Name'),
        ('email', 'Email'),
        ('company', 'Company'),
        ('phone', 'Phone')
    ], default='all')
    
    status_filter = SelectField('Status', choices=[
        ('', 'All Statuses'),
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal_sent', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
        ('on_hold', 'On Hold')
    ])
    
    specialty_filter = SelectField('Specialty', choices=[
        ('', 'All Specialties'),
        ('mental_health', 'Mental Health'),
        ('behavioral_health', 'Behavioral Health'),
        ('clinical_psychology', 'Clinical Psychology'),
        ('family_medicine', 'Family Medicine'),
        ('internal_medicine', 'Internal Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('orthopedics', 'Orthopedics'),
        ('other', 'Other')
    ])
    
    submit = SubmitField('Search')
