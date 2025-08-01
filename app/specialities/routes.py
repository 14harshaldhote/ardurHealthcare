from flask import render_template, jsonify, abort, redirect, url_for, current_app
import json
import os
from . import specialities
from functools import lru_cache

@lru_cache(maxsize=1)
def load_specialty_data():
    """Load specialty data from JSON file"""
    try:
        json_path = os.path.join(current_app.root_path, '..', 'data', 'specialty', 'specialty_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        current_app.logger.error(f"Error loading specialty data: {e}")
        return {"services": {}}

def get_specialty_url_mapping():
    """Map URL slugs to JSON keys"""
    return {
        'mental-health-billing-services': 'mental_health',
        'behavioral-health-billing-services': 'behavioral_health',
        'clinical-psychology-billing-services': 'clinical_psychology',
        'chiropractic-billing-services': 'chiropractic',
        'family-practice-billing-services': 'family_practice',
        'home-health-billing-services': 'home_health',
        'wound-care-billing-services': 'wound_care',
        'physical-therapy-billing-services': 'physical_therapy',
        'massage-therapy-billing-services': 'massage_therapy',
        'podiatry-billing-services': 'podiatry'
    }

def create_fallback_specialty(slug):
    """Create a fallback specialty object if not found in JSON"""
    service_name = slug.replace('-billing-services', '').replace('-', ' ').title()
    return {
        'specialty': f"{service_name} Billing Services",
        'meta_title': f"{service_name} Billing Services | Ardur Healthcare",
        'h1': f"{service_name} Billing Services",
        'description': f"Expert billing support and solutions for {service_name.lower()} providers.",
        'is_fallback': True,
        'services': [], 'challenges': [], 'solutions': [], 'process': [], 'who_we_help': [], 'faqs': []
    }

# This route for the main page is unchanged
@specialities.route('/')
def specialities_main():
    """Main specialities page showing all available specialties"""
    specialty_data = load_specialty_data()
    priority_services = ["Mental Health", "Behavioral Health", "Clinical Psychology", "Chiropractic", "Family Practice", "Home Health", "Wound Care", "Physical Therapy", "Massage Therapy", "Podiatry"]
    json_specialty_names = sorted([name.replace('_', ' ').title() for name in specialty_data.get('services', {}).keys()])
    additional_services = ["Allergy and Immunology", "Ambulatory Surgical Center", "Anesthesia", "Cardiology", "Dental", "Dermatology", "Durable Medical Equipment (DME)", "Emergency Room", "Endocrinology", "Gastroenterology", "General Surgery", "Hospice", "Internal Medicine", "Laboratory", "Neurology", "OB GYN", "Occupational Therapy", "Oncology", "Optometry", "Oral and Maxillofacial", "Orthopedic", "Otolaryngology (ENT)", "Pain Management", "Pathology", "Pediatrics", "Pharmacy", "Plastic Surgery", "Primary Care", "Pulmonology", "Radiation Oncology", "Radiology", "Rheumatology", "Skilled Nursing Facility (SNF)", "Sleep Disorder", "Sports Medicine", "Urgent Care", "Urology"]
    
    seen = set(json_specialty_names)
    main_services = json_specialty_names + [s for s in additional_services if s not in seen]
    main_services = sorted(main_services)

    return render_template('specialities/specialities.html',
                         title='Specialty-Specific Medical Billing Services',
                         specialties=specialty_data.get('services', {}),
                         main_services=main_services,
                         priority_services=priority_services)

# === Dynamic Specialty Page Handler ===
@specialities.route('/<specialty_slug>')
def specialty_page(specialty_slug):
    """Dynamic specialty detail route"""
    specialties_data = load_specialty_data()
    url_mapping = get_specialty_url_mapping()

    # Handle any URL normalization
    if not specialty_slug.endswith('-billing-services'):
        return redirect(url_for('specialities.specialty_page', 
                              specialty_slug=f"{specialty_slug}-billing-services"), 
                      code=301)

    json_key = url_mapping.get(specialty_slug)
    
    # First check if the service exists in our data
    specialty = specialties_data.get('services', {}).get(json_key)
    
    # Only use fallback if we don't have data
    if not specialty:
        specialty = create_fallback_specialty(specialty_slug)

    return render_template('specialities/specialty_detail.html',
                         title=specialty.get('meta_title', ''),
                         meta_description=specialty.get('meta_description', ''),
                         specialty=specialty)


# === Redirect Aliases for Backward Compatibility ===
@specialities.route('/mental-health')
@specialities.route('/mental_health')
def redirect_mental_health():
    return redirect(url_for('specialities.specialty_page', specialty_slug='mental-health-billing-services'), code=301)

@specialities.route('/behavioral-health')
@specialities.route('/behavioral_health')
def redirect_behavioral_health():
    return redirect(url_for('specialities.specialty_page', specialty_slug='behavioral-health-billing-services'), code=301)

@specialities.route('/clinical-psychology')
@specialities.route('/clinical_psychology')
def redirect_clinical_psychology():
    return redirect(url_for('specialities.specialty_page', specialty_slug='clinical-psychology-billing-services'), code=301)

@specialities.route('/chiropractic')
def redirect_chiropractic():
    return redirect(url_for('specialities.specialty_page', specialty_slug='chiropractic-billing-services'), code=301)

# API routes
@specialities.route('/api/specialities')
def api_specialities():
    """API endpoint to get all specialties data"""
    specialties = load_specialty_data()
    return jsonify(specialties)

@specialities.route('/api/specialities/<specialty_slug>')
def api_specialty_detail(specialty_slug):
    """API endpoint to get specific specialty data"""
    specialties_data = load_specialty_data()
    if not specialty_slug.endswith('-billing-services'):
        specialty_slug = f"{specialty_slug}-billing-services"
    
    json_key = get_specialty_url_mapping().get(specialty_slug)
    specialty_data = specialties_data.get('services', {}).get(json_key)
    
    if not specialty_data:
        specialty_data = create_fallback_specialty(specialty_slug)
    
    return jsonify(specialty_data)