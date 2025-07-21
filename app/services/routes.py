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

@services.route('/')
def index():
    """Main services page showing all services"""
    return render_template('billing.html')

@services.route('/<service_name>')
def service_detail(service_name):
    """Dynamic route for individual service pages"""
    services_data = load_services_data()

    # Check if the service exists
    if service_name not in services_data.get('services', {}):
        abort(404)

    service = services_data['services'][service_name]
    return render_template('service_detail.html', service=service, service_name=service_name)

# Legacy routes for backward compatibility
@services.route('/enrollment')
def enrollment():
    """Legacy route - redirects to provider_credentialing"""
    return redirect(url_for('services.service_detail', service_name='provider_credentialing'))

@services.route('/verification')
def verification():
    """Legacy route - redirects to eligibility_verification"""
    return redirect(url_for('services.service_detail', service_name='eligibility_verification'))

@services.route('/billing')
def billing():
    """Medical billing overview page"""
    return render_template('billing.html')

@services.route('/accounts_receivable')
def accounts_receivable():
    """Legacy route - redirects to ar_management"""
    return redirect(url_for('services.service_detail', service_name='ar_management'))

# denial_management route removed - conflicts with dynamic route since it exists in JSON

@services.route('/payment_posting')
def payment_posting():
    """Legacy route - redirects to payment_posting_reconciliation"""
    return redirect(url_for('services.service_detail', service_name='payment_posting_reconciliation'))

# Additional service routes for easy access
@services.route('/eligibility-verification')
def eligibility_verification():
    return redirect(url_for('services.service_detail', service_name='eligibility_verification'))

@services.route('/prior-authorization')
def prior_authorization():
    return redirect(url_for('services.service_detail', service_name='prior_authorization'))

@services.route('/provider-credentialing')
def provider_credentialing():
    return redirect(url_for('services.service_detail', service_name='provider_credentialing'))

@services.route('/charge-entry')
def charge_entry():
    return redirect(url_for('services.service_detail', service_name='charge_entry'))

@services.route('/medical-coding')
def medical_coding():
    return redirect(url_for('services.service_detail', service_name='medical_coding'))

@services.route('/claim-submission')
def claim_submission():
    return redirect(url_for('services.service_detail', service_name='claim_submission_follow_up'))

@services.route('/payment-posting-reconciliation')
def payment_posting_reconciliation():
    return redirect(url_for('services.service_detail', service_name='payment_posting_reconciliation'))

@services.route('/ar-management')
def ar_management():
    return redirect(url_for('services.service_detail', service_name='ar_management'))

# Error handlers
@services.errorhandler(404)
def service_not_found(error):
    """Handle 404 errors for service pages"""
    return render_template('errors/404.html',
                         message="The requested service was not found."), 404
