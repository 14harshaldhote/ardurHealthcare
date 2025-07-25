from flask import render_template, abort, current_app, redirect, url_for
import json
import os
from . import services

def load_services_data():
    """Load services data from JSON file"""
    try:
        json_path = os.path.join(current_app.root_path, '..', 'data', 'services', 'services_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        current_app.logger.error(f"Error loading services data: {e}")
        return {"services": {}}

def get_service_url_mapping():
    """Map URL slugs to JSON keys"""
    return {
        'eligibility-and-benefits-verification-services': 'eligibility_verification',
        'prior-authorization-services': 'prior_authorization',
        'provider-credentialing-and-enrollment-services': 'provider_credentialing',
        'charge-entry-services': 'charge_entry',
        'medical-coding-services': 'medical_coding',
        'claim-submission-and-follow-up-services': 'claim_submission_follow_up',
        'payment-posting-and-reconciliation-services': 'payment_posting_reconciliation',
        'denial-management-services': 'denial_management',
        'accounts-receivable-management-services': 'accounts_receivable_management',
        'medical-billing-services': 'medical_billing_services'
    }

# === Main Pages ===
@services.route('/')
def index():
    """Main services page"""
    return render_template('billing.html')

# === Dynamic Service Page Handler ===
@services.route('/<service_name>')
def service_detail(service_name):
    """Dynamic service detail route"""
    services_data = load_services_data()
    url_mapping = get_service_url_mapping()

    # Handle the inconsistent URLs from billing.html
    if service_name == 'payment-posting-and-reconciliation':
        service_name = 'payment-posting-and-reconciliation-services'
    elif service_name == 'accounts-receivable-management':
        service_name = 'accounts-receivable-management-services'

    json_key = url_mapping.get(service_name)

    if not json_key or json_key not in services_data.get('services', {}):
        abort(404)

    service = services_data['services'][json_key]
    return render_template('service_detail.html', service=service, service_name=service_name)

# === Redirect Aliases for Backward Compatibility ===

@services.route('/enrollment')
@services.route('/provider-credentialing')
@services.route('/provider_credentialing')
def redirect_provider_credentialing():
    return redirect(url_for('services.service_detail', service_name='provider-credentialing-and-enrollment-services'), code=301)

@services.route('/verification')
@services.route('/eligibility-verification')
@services.route('/eligibility_verification')
def redirect_eligibility():
    return redirect(url_for('services.service_detail', service_name='eligibility-and-benefits-verification-services'), code=301)

@services.route('/prior-authorization')
@services.route('/prior_authorization')
def redirect_prior_auth():
    return redirect(url_for('services.service_detail', service_name='prior-authorization-services'), code=301)

@services.route('/charge-entry')
@services.route('/charge_entry')
def redirect_charge_entry():
    return redirect(url_for('services.service_detail', service_name='charge-entry-services'), code=301)

@services.route('/medical-coding')
@services.route('/medical_coding')
def redirect_medical_coding():
    return redirect(url_for('services.service_detail', service_name='medical-coding-services'), code=301)

@services.route('/claim-submission')
@services.route('/claim_submission_follow_up')
@services.route('/claim-submission-follow-up')
def redirect_claim_submission():
    return redirect(url_for('services.service_detail', service_name='claim-submission-and-follow-up-services'), code=301)

@services.route('/payment-posting')
@services.route('/payment_posting')
@services.route('/payment-posting-reconciliation')
@services.route('/payment_posting_reconciliation')
@services.route('/payment-posting-and-reconciliation')
def redirect_payment_posting():
    return redirect(url_for('services.service_detail', service_name='payment-posting-and-reconciliation-services'), code=301)

@services.route('/denial-management')
@services.route('/denial_management')
def redirect_denial_management():
    return redirect(url_for('services.service_detail', service_name='denial-management-services'), code=301)

@services.route('/accounts-receivable')
@services.route('/accounts_receivable')
@services.route('/ar-management')
@services.route('/ar_management')
@services.route('/accounts-receivable-management')
def redirect_ar_management():
    return redirect(url_for('services.service_detail', service_name='accounts-receivable-management-services'), code=301)

@services.route('/medical-billing')
@services.route('/medical_billing')
def redirect_medical_billing():
    return redirect(url_for('services.service_detail', service_name='medical-billing-services'), code=301)

# === 404 Error Handler ===
@services.errorhandler(404)
def service_not_found(error):
    return render_template('errors/404.html',
                           message="The requested service was not found."), 404
