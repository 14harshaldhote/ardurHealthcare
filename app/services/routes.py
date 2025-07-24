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
        'eligibility-and-benefits-verification': 'eligibility_verification',
        'prior-authorization-services': 'prior_authorization',
        'provider-credentialing-and-enrollment': 'provider_credentialing',
        'charge-entry-services': 'charge_entry',
        'medical-coding-services': 'medical_coding',
        'claim-submission-and-follow-up-services': 'claim_submission_follow_up',
        'payment-posting-and-reconciliation': 'payment_posting_reconciliation',
        'denial-management-services': 'denial_management',
        'accounts-receivable-management': 'ar_management'
    }

@services.route('/')
def index():
    """Main services page showing all services"""
    return render_template('billing.html')

@services.route('/<service_name>')
def service_detail(service_name):
    """Dynamic route for individual service pages"""
    services_data = load_services_data()
    url_mapping = get_service_url_mapping()

    # Get the JSON key for this URL slug
    json_key = url_mapping.get(service_name)

    # If no direct mapping found, try the old underscore conversion for backward compatibility
    if not json_key:
        json_key = service_name.replace('-', '_')

    # Check if the service exists
    if json_key not in services_data.get('services', {}):
        abort(404)

    service = services_data['services'][json_key]
    return render_template('service_detail.html', service=service, service_name=service_name)

# Legacy routes for backward compatibility
@services.route('/enrollment')
def enrollment():
    """Legacy route - redirects to provider credentialing"""
    return redirect(url_for('services.service_detail', service_name='provider-credentialing-and-enrollment'))

@services.route('/verification')
def verification():
    """Legacy route - redirects to eligibility verification"""
    return redirect(url_for('services.service_detail', service_name='eligibility-and-benefits-verification'))

@services.route('/billing')
def billing():
    """Medical billing overview page"""
    return render_template('billing.html')

@services.route('/accounts_receivable')
def accounts_receivable():
    """Legacy route - redirects to accounts-receivable-management"""
    return redirect(url_for('services.service_detail', service_name='accounts-receivable-management'))

# denial_management route removed - conflicts with dynamic route since it exists in JSON

@services.route('/payment_posting')
def payment_posting():
    """Legacy route - redirects to payment-posting-and-reconciliation"""
    return redirect(url_for('services.service_detail', service_name='payment-posting-and-reconciliation'))

# Additional service routes for easy access and backward compatibility
@services.route('/eligibility-verification')
def eligibility_verification():
    return redirect(url_for('services.service_detail', service_name='eligibility-and-benefits-verification'))

@services.route('/prior-authorization')
def prior_authorization():
    return redirect(url_for('services.service_detail', service_name='prior-authorization-services'))

@services.route('/provider-credentialing')
def provider_credentialing():
    return redirect(url_for('services.service_detail', service_name='provider-credentialing-and-enrollment'))

@services.route('/charge-entry')
def charge_entry():
    return redirect(url_for('services.service_detail', service_name='charge-entry-services'))

@services.route('/medical-coding')
def medical_coding():
    return redirect(url_for('services.service_detail', service_name='medical-coding-services'))

@services.route('/claim-submission')
def claim_submission():
    return redirect(url_for('services.service_detail', service_name='claim-submission-and-follow-up-services'))

@services.route('/payment-posting-reconciliation')
def payment_posting_reconciliation():
    return redirect(url_for('services.service_detail', service_name='payment-posting-and-reconciliation'))

@services.route('/ar-management')
def ar_management():
    return redirect(url_for('services.service_detail', service_name='accounts-receivable-management'))

# Old underscore-based routes for backward compatibility
@services.route('/eligibility_verification')
def eligibility_verification_old():
    return redirect(url_for('services.service_detail', service_name='eligibility-and-benefits-verification'))

@services.route('/prior_authorization')
def prior_authorization_old():
    return redirect(url_for('services.service_detail', service_name='prior-authorization-services'))

@services.route('/provider_credentialing')
def provider_credentialing_old():
    return redirect(url_for('services.service_detail', service_name='provider-credentialing-and-enrollment'))

@services.route('/charge_entry')
def charge_entry_old():
    return redirect(url_for('services.service_detail', service_name='charge-entry-services'))

@services.route('/medical_coding')
def medical_coding_old():
    return redirect(url_for('services.service_detail', service_name='medical-coding-services'))

@services.route('/claim_submission_follow_up')
def claim_submission_follow_up_old():
    return redirect(url_for('services.service_detail', service_name='claim-submission-and-follow-up-services'))

@services.route('/payment_posting_reconciliation')
def payment_posting_reconciliation_old():
    return redirect(url_for('services.service_detail', service_name='payment-posting-and-reconciliation'))

@services.route('/denial_management')
def denial_management_old():
    return redirect(url_for('services.service_detail', service_name='denial-management-services'))

@services.route('/ar_management')
def ar_management_old():
    return redirect(url_for('services.service_detail', service_name='accounts-receivable-management'))

# All service routes are now handled by the dynamic route above
# The JSON data contains all the necessary SEO and content information

# Error handlers
@services.errorhandler(404)
def service_not_found(error):
    """Handle 404 errors for service pages"""
    return render_template('errors/404.html',
                         message="The requested service was not found."), 404
