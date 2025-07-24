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

    # Convert hyphenated URL to underscore format for JSON lookup
    json_key = service_name.replace('-', '_')

    # Check if the service exists
    if json_key not in services_data.get('services', {}):
        abort(404)

    service = services_data['services'][json_key]
    return render_template('service_detail.html', service=service, service_name=service_name)

# Legacy routes for backward compatibility
@services.route('/enrollment')
def enrollment():
    """Legacy route - redirects to provider_credentialing"""
    return redirect(url_for('services.service_detail', service_name='provider-credentialing-and-enrollment'))

@services.route('/verification')
def verification():
    """Legacy route - redirects to eligibility_verification"""
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

# Additional service routes for easy access
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

# Specific service routes with SEO data
@services.route('/eligibility-and-benefits-verification')
def eligibility_benefits_verification():
    """Eligibility and Benefits Verification Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Eligibility and Benefits Verification Services',
                             'meta_title': 'Eligibility and Benefits Verification Services | Ardur Healthcare',
                             'meta_description': 'Ensure real-time eligibility and benefits verification for all payers. Reduce claim denials and improve collections with Ardur\'s expert verification services.',
                             'h1': 'Eligibility and Benefits Verification Services',
                             'h2_sections': [
                                 'Optimize Revenue with Pre-Service Eligibility Checks',
                                 'Our Eligibility Verification Process',
                                 'Why Choose Ardur Healthcare for Benefits Verification?',
                                 'Ready to Eliminate Coverage Guesswork?',
                                 'FAQs about Our Eligibility and Benefits Verification Services'
                             ]
                         },
                         service_name='eligibility_benefits_verification')

@services.route('/prior-authorization-services')
def prior_authorization_services():
    """Prior Authorization Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Prior Authorization Services',
                             'meta_title': 'Prior Authorization Services | Ardur Healthcare',
                             'meta_description': 'Prior authorization services that reduce delays and denials. We handle medication and procedure approvals quickly to keep your revenue cycle on track.',
                             'h1': 'Prior Authorization Services',
                             'h2_sections': [
                                 'Eliminate Authorization Delays with Expert Support',
                                 'Our Prior Authorization Process',
                                 'Why Choose Ardur Healthcare for Prior Authorizations?',
                                 'Ready to Improve Your Approval Rates?',
                                 'FAQs about Our Prior Authorization Services'
                             ]
                         },
                         service_name='prior_authorization_services')

@services.route('/provider-credentialing-and-enrollment')
def provider_credentialing_enrollment():
    """Provider Credentialing and Enrollment Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Provider Credentialing and Enrollment Services',
                             'meta_title': 'Provider Credentialing and Enrollment Services | Ardur Healthcare',
                             'meta_description': 'Accelerate payer approvals and reduce delays with expert provider credentialing and enrollment services. Get started with Ardur Healthcare today.',
                             'h1': 'Provider Credentialing and Enrollment Services',
                             'h2_sections': [
                                 'Efficient Credentialing That Keeps You In-Network',
                                 'Our Credentialing & Enrollment Process',
                                 'Why Choose Ardur Healthcare for Provider Credentialing?',
                                 'Ready to Accelerate Your Payer Enrollment?',
                                 'FAQs about Our Provider Credentialing & Enrollment Services'
                             ]
                         },
                         service_name='provider_credentialing_enrollment')

@services.route('/charge-entry-services')
def charge_entry_services():
    """Charge Entry Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Charge Entry Services',
                             'meta_title': 'Charge Entry Services | Ardur Healthcare',
                             'meta_description': 'Improve billing accuracy and speed up reimbursements with Ardur Healthcare\'s expert charge entry services. Start your clean claims journey with us today.',
                             'h1': 'Charge Entry Services',
                             'h2_sections': [
                                 'Precision-Driven Charge Entry in Medical Billing',
                                 'Our Charge Entry Process',
                                 'Why Choose Ardur Healthcare for Charge Entry?',
                                 'Let\'s Eliminate Revenue Leaks at the Start',
                                 'FAQs about Our Charge Entry Services'
                             ]
                         },
                         service_name='charge_entry_services')

@services.route('/medical-coding-services')
def medical_coding_services():
    """Medical Coding Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Medical Coding Services',
                             'meta_title': 'Medical Coding Services | Ardur Healthcare',
                             'meta_description': 'Ensure clean claims and full compliance with Ardur Healthcare\'s medical coding services. Certified coders, specialty expertise, and audit-ready processes.',
                             'h1': 'Medical Coding Services',
                             'h2_sections': [
                                 'Medical Coding That Powers Your Revenue Cycle',
                                 'Our Medical Coding Process',
                                 'Why Choose Ardur Healthcare for Medical Coding?',
                                 'Ready for Cleaner Claims and Higher Reimbursements?',
                                 'FAQs about Our Medical Coding Services'
                             ]
                         },
                         service_name='medical_coding_services')

@services.route('/claim-submission-and-follow-up-services')
def claim_submission_follow_up_services():
    """Claim Submission and Follow-Up Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Claim Submission and Follow-Up Services',
                             'meta_title': 'Claim Submission and Follow-Up Services | Ardur Healthcare',
                             'meta_description': 'Speed up payments and reduce denials with Ardur Healthcare\'s claim submission and follow-up services. Clean claims, real-time tracking, and expert AR follow-up.',
                             'h1': 'Claim Submission and Follow-Up Services',
                             'h2_sections': [
                                 'Precision-Driven Claim Submission & Tracking',
                                 'Our Claim Submission and Follow-Up Process',
                                 'Why Choose Ardur Healthcare for Claim Submission?',
                                 'Ready to Strengthen Your Claim Lifecycle?',
                                 'FAQs about Our Claim Submission and Follow-Up Services'
                             ]
                         },
                         service_name='claim_submission_follow_up_services')

@services.route('/payment-posting-and-reconciliation')
def payment_posting_reconciliation_services():
    """Payment Posting and Reconciliation Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Payment Posting and Reconciliation Services',
                             'meta_title': 'Payment Posting and Reconciliation Services | Ardur Healthcare',
                             'meta_description': 'Ensure accurate payment posting and reconciliation with Ardur Healthcare. We post ERAs, EOBs, and patient payments with speed and precision.',
                             'h1': 'Payment Posting and Reconciliation Services',
                             'h2_sections': [
                                 'Precision-Driven Payment Posting for Reliable Revenue',
                                 'Our Payment Posting and Reconciliation Process',
                                 'Why Providers Trust Ardur for Payment Posting?',
                                 'Clean Records. Faster Revenue. Clear Insights.',
                                 'FAQs about Our Payment Posting and Reconciliation Services'
                             ]
                         },
                         service_name='payment_posting_reconciliation_services')

@services.route('/denial-management-services')
def denial_management_services():
    """Denial Management Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Denial Management Services',
                             'meta_title': 'Denial Management Services | Ardur Healthcare',
                             'meta_description': 'Recover lost revenue with Ardur Healthcare\'s denial management services. We resolve, appeal, and prevent medical billing denials across all payers.',
                             'h1': 'Denial Management Services',
                             'h2_sections': [
                                 'End-to-End Claim Denial Management for Healthcare Providers',
                                 'Our Denial Management Process',
                                 'Why Choose Ardur for Denials Management?',
                                 'Don\'t Let Denials Drain Your Revenue',
                                 'FAQs about Our Denial Management Services'
                             ]
                         },
                         service_name='denial_management_services')

@services.route('/accounts-receivable-management')
def accounts_receivable_management_services():
    """Accounts Receivable Management Services page"""
    return render_template('service_detail.html',
                         service={
                             'title': 'Accounts Receivable Management Services',
                             'meta_title': 'Accounts Receivable Management Services | Ardur Healthcare',
                             'meta_description': 'Streamline collections and reduce claim aging with Ardur Healthcare\'s accounts receivable management services. Improve your cash flow with proven AR strategies.',
                             'h1': 'Accounts Receivable Management Services',
                             'h2_sections': [
                                 'Complete AR Management for Healthcare Providers',
                                 'Our Accounts Receivable Management Process',
                                 'Why Choose Ardur for Accounts Receivable Management?',
                                 'Take Control of Your Receivables Today',
                                 'FAQs about Our Accounts Receivable Management Services'
                             ]
                         },
                         service_name='accounts_receivable_management_services')

# Error handlers
@services.errorhandler(404)
def service_not_found(error):
    """Handle 404 errors for service pages"""
    return render_template('errors/404.html',
                         message="The requested service was not found."), 404
