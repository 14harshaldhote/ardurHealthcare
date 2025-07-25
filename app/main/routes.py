# app/main/routes.py
from flask import render_template, redirect, url_for
import json
import os
from datetime import datetime
from flask import render_template, url_for, redirect, current_app, Response
from . import main


def load_specialty_data():
    """Load specialty data from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'specialty', 'specialty_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('services', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_services_data():
    """Load services data from JSON file for sitemap"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'services', 'services_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('services', {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_state_data():
    """Load state data from JSON files for sitemap"""
    state_data = {}
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'states')

    json_files = [
        'state_data.json',
        'additional_states.json',
        'more_states.json'
    ]

    for json_file in json_files:
        file_path = os.path.join(data_dir, json_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state_data.update(data)
            except (FileNotFoundError, json.JSONDecodeError):
                continue

    return state_data


def get_all_blog_posts():
    """Get all blog posts for sitemap"""
    try:
        from ..resources.blog_data import get_all_blog_posts
        return get_all_blog_posts()
    except ImportError:
        return []


def generate_state_url_slug(state_name):
    """Generate URL slug from state name using ourreach module logic"""
    # Use underscores to match JSON data structure, then add the prefix
    state_slug = state_name.lower().replace(' ', '_').replace(',', '').replace('.', '')
    return f"medical-billing-services-in-{state_slug}"


def get_service_url_mapping():
    """Map URL slugs to JSON keys - imported from services module logic"""
    return {
        'eligibility-and-benefits-verification-services': 'eligibility_verification',
        'prior-authorization-services': 'prior_authorization',
        'provider-credentialing-and-enrollment-services': 'provider_credentialing',
        'charge-entry-services': 'charge_entry',
        'medical-coding-services': 'medical_coding',
        'claim-submission-and-follow-up-services': 'claim_submission_follow_up',
        'payment-posting-and-reconciliation-services': 'payment_posting_reconciliation',
        'denial-management-services': 'denial_management',
        'accounts-receivable-management-services': 'ar_management',
        'medical-billing-services': 'medical_billing'
    }


def create_specialty_url_slug(specialty_name):
    """Create URL-friendly slug from specialty name"""
    return specialty_name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '-').replace('&', 'and')


def get_route_priority_and_changefreq(endpoint, url):
    """Determine priority and change frequency based on route patterns"""
    # Home page
    if endpoint == 'main.home' or url == '/':
        return '1.00', 'daily'

    # Key static pages
    key_pages = ['main.about', 'main.services', 'contact.contact_form', 'main.privacy_policy']
    if endpoint in key_pages:
        return '0.80', 'monthly'

    # Blog posts and resources
    if 'resources.blog' in endpoint or 'resources.' in endpoint:
        return '0.60', 'weekly'

    # Services and specialties
    if 'services.' in endpoint or 'specialities.' in endpoint:
        return '0.70', 'monthly'

    # State pages
    if 'ourreach.' in endpoint:
        return '0.60', 'monthly'

    # Analytics and auth pages (lower priority)
    if 'analytics.' in endpoint or 'auth.' in endpoint:
        return '0.30', 'yearly'

    # Default for other pages
    return '0.50', 'monthly'

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


@main.route('/sitemap.xml')
def sitemap():
    """Generate dynamic XML sitemap for all routes"""

    base_url = 'https://ardurhealthcare.com'
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Start XML sitemap
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

    # Get all registered routes
    urls_added = set()  # Track URLs to avoid duplicates

    for rule in current_app.url_map.iter_rules():
        # Skip routes that require parameters we can't generate
        if 'GET' not in rule.methods:
            continue

        # Skip admin/auth routes for public sitemap
        if any(skip in rule.endpoint for skip in ['auth.', 'analytics.']):
            continue

        try:
            # Handle static routes (no parameters)
            if not rule.arguments:
                url = url_for(rule.endpoint, _external=False)
                if url not in urls_added:
                    priority, changefreq = get_route_priority_and_changefreq(rule.endpoint, url)
                    xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
                    urls_added.add(url)

            # Handle dynamic routes with parameters
            else:
                # Blog post routes
                if 'resources.blog_post' in rule.endpoint:
                    blog_posts = get_all_blog_posts()
                    for post in blog_posts:
                        url = url_for(rule.endpoint, slug=post['slug'], _external=False)
                        if url not in urls_added:
                            priority, changefreq = get_route_priority_and_changefreq(rule.endpoint, url)
                            xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
                            urls_added.add(url)

                # Service detail routes
                elif 'services.service_detail' in rule.endpoint:
                    url_mapping = get_service_url_mapping()
                    for service_slug in url_mapping.keys():
                        try:
                            url = url_for(rule.endpoint, service_name=service_slug, _external=False)
                            if url not in urls_added:
                                priority, changefreq = get_route_priority_and_changefreq(rule.endpoint, url)
                                xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
                                urls_added.add(url)
                        except Exception as e:
                            current_app.logger.warning(f"Could not generate service URL for {service_slug}: {str(e)}")
                            continue

                # Specialty routes
                elif 'specialities.specialty' in rule.endpoint and 'detail' not in rule.endpoint:
                    specialty_data = load_specialty_data()
                    for specialty in specialty_data:
                        # Create slug from specialty name
                        specialty_slug = create_specialty_url_slug(specialty['specialty'])
                        try:
                            url = url_for(rule.endpoint, specialty_type=specialty_slug, _external=False)
                            if url not in urls_added:
                                priority, changefreq = get_route_priority_and_changefreq(rule.endpoint, url)
                                xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
                                urls_added.add(url)
                        except Exception as e:
                            current_app.logger.warning(f"Could not generate specialty URL for {specialty_slug}: {str(e)}")
                            continue

                # State pages
                elif 'ourreach.state_page' in rule.endpoint:
                    state_data = load_state_data()
                    for state_key, state_info in state_data.items():
                        state_slug = generate_state_url_slug(state_info['name'])
                        try:
                            url = url_for(rule.endpoint, state_slug=state_slug, _external=False)
                            if url not in urls_added:
                                priority, changefreq = get_route_priority_and_changefreq(rule.endpoint, url)
                                xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
                                urls_added.add(url)
                        except Exception as e:
                            current_app.logger.warning(f"Could not generate state URL for {state_slug}: {str(e)}")
                            continue

        except Exception as e:
            # Log error but continue processing other routes
            current_app.logger.warning(f"Could not generate sitemap URL for {rule.endpoint}: {str(e)}")
            continue

    # Add hardcoded specific blog routes that might not be caught by dynamic routing
    specific_blog_posts = [
        'what-is-medical-billing',
        'medical-coding-vs-billing',
        'medical-billing-denial-reasons',
        'cpt-icd10-hcpcs-codes',
        'medical-billing-process-overview'
    ]

    for slug in specific_blog_posts:
        url = f'/resources/blog/{slug}'
        if url not in urls_added:
            xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.60</priority>
  </url>
'''
            urls_added.add(url)

    # Add hardcoded specialty routes that have specific endpoints
    specific_specialty_routes = [
        'mental-health-billing-services',
        'behavioral-health-billing-services',
        'clinical-psychology-billing-services',
        'chiropractic-billing-services',
        'family-practice-billing-services',
        'home-health-billing-services',
        'podiatry-billing-services',
        'wound-care-billing-services',
        'physical-therapy-billing-services',
        'massage-therapy-billing-services'
    ]

    for specialty_slug in specific_specialty_routes:
        url = f'/specialty/{specialty_slug}'
        if url not in urls_added:
            xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.70</priority>
  </url>
'''
            urls_added.add(url)

    # Close XML sitemap
    xml_content += '</urlset>'

    return Response(xml_content, mimetype='application/xml')
