from flask import render_template, jsonify, abort
import json
import os
from . import specialities

def load_specialty_data():
    """Load specialty data from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'specialty', 'specialty_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('services', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def create_url_slug(specialty_name):
    """Create URL-friendly slug from specialty name"""
    return specialty_name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '-').replace('&', 'and')

def get_specialty_by_slug(slug):
    """Get specialty data by URL slug"""
    specialties = load_specialty_data()

    # First try exact match with full specialty name
    for specialty in specialties:
        if create_url_slug(specialty['specialty']) == slug:
            return specialty

    # Try matching with clean name (without " Billing Services")
    for specialty in specialties:
        clean_name = specialty['specialty'].replace(' Billing Services', '').strip()
        if create_url_slug(clean_name) == slug:
            # Return specialty data but use clean name for display
            specialty_copy = specialty.copy()
            specialty_copy['specialty'] = clean_name
            return specialty_copy

    # If no match found, create a basic specialty object
    service_name = slug.replace('-', ' ').title()

    # Create a basic specialty object for services not in JSON
    basic_specialty = {
        'specialty': service_name,
        'description': f'Professional medical billing services for {service_name.lower()} providers with expertise in specialty-specific coding, compliance, and revenue optimization.',
        'services': [
            'Insurance Verification & Authorization',
            'Specialty-Specific Claims Processing',
            'Payment Posting & Reconciliation',
            'Denial Management & Appeals',
            'Accounts Receivable Follow-up',
            'Coding & Documentation Review',
            'Compliance Monitoring',
            'Revenue Cycle Optimization'
        ],
        'challenges': [
            f'Complex {service_name.lower()} coding requirements and guidelines',
            'Frequent claim denials due to documentation issues',
            'Time-consuming prior authorization processes',
            'Keeping up with changing regulations and payer policies',
            'Managing high accounts receivable balances'
        ],
        'solutions': [
            f'Expert {service_name.lower()}-specific coding and documentation',
            'Proactive denial management and appeals process',
            'Streamlined prior authorization workflows',
            'Real-time eligibility verification systems',
            'Dedicated follow-up specialists for faster collections'
        ],
        'process': [
            'Insurance Verification',
            'Patient Registration & Demographics',
            'Coding & Documentation Review',
            'Claims Submission & Tracking',
            'Payment Processing & Posting',
            'Follow-up & Collections',
            'Reporting & Analytics'
        ],
        'who_we_help': [
            f'{service_name} Specialists',
            'Private Practice Physicians',
            'Medical Groups & Clinics',
            'Healthcare Systems',
            'Solo Practitioners',
            'Multi-location Practices'
        ],
        'faqs': [
            {
                'question': f'What {service_name.lower()} billing services do you provide?',
                'answer': f'We provide comprehensive billing services for {service_name.lower()} providers including insurance verification, specialty-specific claims processing, payment posting, denial management, and accounts receivable follow-up. Our team understands the unique coding and billing requirements for {service_name.lower()} practices.'
            },
            {
                'question': 'How do you ensure accurate coding and compliance?',
                'answer': f'Our certified coding specialists have extensive experience with {service_name.lower()} procedures and stay current with the latest coding guidelines, payer requirements, and regulatory changes to ensure accurate claim submission and compliance.'
            },
            {
                'question': 'What is your average collection rate?',
                'answer': 'We typically achieve collection rates of 95-98% for our clients through proactive follow-up, expert denial management, and our proven revenue cycle optimization strategies.'
            },
            {
                'question': 'How quickly can you start billing for my practice?',
                'answer': 'We can typically begin billing for your practice within 1-2 weeks of contract signing, depending on the complexity of your setup and any required credentialing or system integrations.'
            }
        ]
    }

    return basic_specialty

@specialities.route('/specialities')
def specialities_main():
    """Main specialities page showing all available specialties"""
    specialties = load_specialty_data()

    # Priority services (the 10 most popular ones)
    priority_services = [
        "Mental Health",
        "Behavioral Health",
        "Clinical Psychology",
        "Chiropractic",
        "Family Practice",
        "Home Health",
        "Wound Care",
        "Physical Therapy",
        "Massage Therapy",
        "Podiatry"
    ]

    # Create clean specialty names from JSON data (remove " Billing Services" suffix)
    json_specialty_names = []
    for s in specialties:
        clean_name = s['specialty'].replace(' Billing Services', '').strip()
        json_specialty_names.append(clean_name)

    # Additional services not in JSON
    additional_services = [
        "Allergy and Immunology",
        "Ambulatory Surgical Center",
        "Anesthesia",
        "Cardiology",
        "Dental",
        "Dermatology",
        "Durable Medical Equipment (DME)",
        "Emergency Room",
        "Endocrinology",
        "Gastroenterology",
        "General Surgery",
        "Hospice",
        "Internal Medicine",
        "Laboratory",
        "Neurology",
        "OB GYN",
        "Occupational Therapy",
        "Oncology",
        "Optometry",
        "Oral and Maxillofacial",
        "Orthopedic",
        "Otolaryngology (ENT)",
        "Pain Management",
        "Pathology",
        "Pediatrics",
        "Pharmacy",
        "Plastic Surgery",
        "Primary Care",
        "Pulmonology",
        "Radiation Oncology",
        "Radiology",
        "Rheumatology",
        "Skilled Nursing Facility (SNF)",
        "Sleep Disorder",
        "Sports Medicine",
        "Urgent Care",
        "Urology"
    ]

    # Combine JSON specialty names with additional services, avoid duplicates
    main_services = []
    seen = set()

    # Add JSON specialties first (they have priority)
    for name in json_specialty_names:
        if name not in seen:
            main_services.append(name)
            seen.add(name)

    # Add additional services if not already present
    for service in additional_services:
        if service not in seen:
            main_services.append(service)
            seen.add(service)

    # Sort alphabetically
    main_services = sorted(main_services)

    return render_template('specialities/specialities.html',
                         title='Specialty-Specific Medical Billing Services',
                         specialties=specialties,
                         main_services=main_services,
                         priority_services=priority_services)

@specialities.route('/specialities/<specialty_type>')
def specialty(specialty_type):
    """Individual specialty page with dynamic content - matches base template calls"""
    specialty_data = get_specialty_by_slug(specialty_type)

    if not specialty_data:
        abort(404)

    return render_template('specialities/specialty_detail.html',
                         title=specialty_data['specialty'],
                         specialty=specialty_data)

@specialities.route('/specialities/<specialty_slug>/detail')
def specialty_detail(specialty_slug):
    """Alternative route for specialty details"""
    specialty_data = get_specialty_by_slug(specialty_slug)

    if not specialty_data:
        abort(404)

    return render_template('specialities/specialty_detail.html',
                         title=specialty_data['specialty'],
                         specialty=specialty_data)

@specialities.route('/api/specialities')
def api_specialities():
    """API endpoint to get all specialties data"""
    specialties = load_specialty_data()
    return jsonify(specialties)

@specialities.route('/api/specialities/<specialty_slug>')
def api_specialty_detail(specialty_slug):
    """API endpoint to get specific specialty data"""
    specialty_data = get_specialty_by_slug(specialty_slug)

    if not specialty_data:
        abort(404)

    return jsonify(specialty_data)
