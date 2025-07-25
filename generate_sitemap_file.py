#!/usr/bin/env python3
"""
Static Sitemap Generator for Ardur Healthcare

This script generates a static sitemap.xml file that can be saved to disk.
While the Flask app serves the sitemap dynamically at /sitemap.xml,
this script can be used to generate a static file if needed for:
- Search engine submission
- CDN caching
- Backup purposes

Usage:
    python generate_sitemap_file.py
    python generate_sitemap_file.py --output custom_sitemap.xml
"""

import os
import sys
import json
import argparse
from datetime import datetime, UTC

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app


def load_services_data():
    """Load services data from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'services', 'services_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('services', {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_specialty_data():
    """Load specialty data from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'specialty', 'specialty_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('services', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_state_data():
    """Load state data from JSON files"""
    state_data = {}
    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'states')

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
    """Get all blog posts"""
    try:
        from app.resources.blog_data import get_all_blog_posts
        return get_all_blog_posts()
    except ImportError:
        return []


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
        'accounts-receivable-management-services': 'ar_management',
        'medical-billing-services': 'medical_billing'
    }


def create_specialty_url_slug(specialty_name):
    """Create URL-friendly slug from specialty name"""
    return specialty_name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '-').replace('&', 'and')


def generate_state_url_slug(state_name):
    """Generate URL slug from state name using ourreach module logic"""
    state_slug = state_name.lower().replace(' ', '_').replace(',', '').replace('.', '')
    return f"medical-billing-services-in-{state_slug}"


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


def generate_sitemap_xml():
    """Generate the complete sitemap XML content using manual URL building"""

    base_url = 'https://ardurhealthcare.com'
    current_time = datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Start XML sitemap
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

    urls_added = set()  # Track URLs to avoid duplicates

    # Static routes - manually build URLs
    static_routes = [
        ('/', '1.00', 'daily'),
        ('/about-us', '0.80', 'monthly'),
        ('/services', '0.80', 'monthly'),
        ('/contact-us', '0.80', 'monthly'),
        ('/privacy-policy', '0.50', 'yearly'),
        ('/coverage', '0.50', 'monthly'),
        ('/enrollment', '0.50', 'monthly'),
        ('/verification', '0.50', 'monthly'),
        ('/coding', '0.50', 'monthly'),
        ('/claims', '0.50', 'monthly'),
        ('/accounts_receivable', '0.50', 'monthly'),
        ('/services/', '0.70', 'monthly'),
        ('/resources/', '0.60', 'weekly'),
        ('/resources/blog', '0.60', 'weekly'),
        ('/resources/case-studies/', '0.60', 'monthly'),
        ('/resources/faqs/', '0.60', 'monthly'),
        ('/resources/press', '0.50', 'monthly'),
        ('/resources/guidelines', '0.50', 'monthly'),
        ('/specialty/', '0.70', 'monthly'),
        ('/state/', '0.60', 'monthly'),
        ('/state/states', '0.60', 'monthly'),
    ]

    for url, priority, changefreq in static_routes:
        if url not in urls_added:
            xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
            urls_added.add(url)

    # Blog post routes
    blog_posts = get_all_blog_posts()
    for post in blog_posts:
        url = f'/resources/blog/{post["slug"]}'
        if url not in urls_added:
            xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.60</priority>
  </url>
'''
            urls_added.add(url)

    # Specific blog routes that might not be in dynamic data
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

    # Service detail routes
    url_mapping = get_service_url_mapping()
    for service_slug in url_mapping.keys():
        url = f'/services/{service_slug}'
        if url not in urls_added:
            xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.70</priority>
  </url>
'''
            urls_added.add(url)

    # Specialty routes
    specialty_data = load_specialty_data()
    for specialty in specialty_data:
        specialty_slug = create_specialty_url_slug(specialty['specialty'])
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

    # Hardcoded specialty routes that have specific endpoints
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

    # State pages
    state_data = load_state_data()
    for state_key, state_info in state_data.items():
        state_slug = generate_state_url_slug(state_info['name'])
        url = f'/state/{state_slug}'
        if url not in urls_added:
            xml_content += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{current_time}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.60</priority>
  </url>
'''
            urls_added.add(url)

    # Close XML sitemap
    xml_content += '</urlset>'

    return xml_content, len(urls_added)


def main():
    """Main function to generate sitemap file"""
    parser = argparse.ArgumentParser(description='Generate static sitemap.xml file for Ardur Healthcare')
    parser.add_argument('--output', '-o', default='sitemap.xml',
                       help='Output filename (default: sitemap.xml)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress output messages')

    args = parser.parse_args()

    if not args.quiet:
        print("🗺️  Generating sitemap...")

    try:
        xml_content, url_count = generate_sitemap_xml()

        # Write to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        if not args.quiet:
            print(f"✅ Sitemap generated successfully!")
            print(f"📄 File: {args.output}")
            print(f"🔗 URLs: {url_count}")
            print(f"📊 Size: {len(xml_content):,} characters")

            # Show file path
            full_path = os.path.abspath(args.output)
            print(f"📍 Full path: {full_path}")

        return 0

    except Exception as e:
        print(f"❌ Error generating sitemap: {str(e)}")
        return 1


if __name__ == '__main__':
    exit(main())
