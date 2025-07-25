# app/main/routes.py
from flask import render_template, redirect, url_for
import json
import os
from . import main  # Import the blueprint created in app/main/__init__.py

def load_specialty_data():
    """Load specialty data from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'specialty', 'specialty_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('services', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about-us')
def about():
    return render_template('about.html')

@main.route('/services')
def services():
    return redirect(url_for('services.index'))

@main.route('/coverage')
def coverage():
    return redirect(url_for('contact.contact_form'))

@main.route('/enrollment')
def enrollment_redirect():
    return redirect(url_for('services.service_detail', service_name='provider-credentialing-and-enrollment'))

@main.route('/verification')
def verification_redirect():
    return redirect(url_for('services.service_detail', service_name='eligibility-and-benefits-verification'))

@main.route('/coding')
def coding_redirect():
    return redirect(url_for('services.service_detail', service_name='medical-coding-services'))

@main.route('/claims')
def claims_redirect():
    return redirect(url_for('services.service_detail', service_name='claim-submission-and-follow-up-services'))

@main.route('/accounts_receivable')
def accounts_receivable_redirect():
    return redirect(url_for('services.service_detail', service_name='accounts-receivable-management'))




@main.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html',
                         title='Privacy Policy | Ardur Healthcare Medical Billing',
                         meta_description='Learn about privacy policy for Ardur Healthcare. What we collect, how we use collected data. We never share or sell your information to third party.')

@main.route('/privacy-policy/')
def privacy_policy_slash():
    return render_template('privacy_policy.html',
                         title='Privacy Policy | Ardur Healthcare Medical Billing',
                         meta_description='Learn about privacy policy for Ardur Healthcare. What we collect, how we use collected data. We never share or sell your information to third party.')
