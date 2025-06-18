# app/specialities/routes.py
from flask import render_template, Blueprint
from flask_login import login_required

from . import specialities

@specialities.route('/specialities/<specialty_type>')
def specialty(specialty_type):
    # Map specialty types to their details
    specialty_details = {
        'family-practice': {
            'title': 'Family Practice',
            'description': 'Comprehensive healthcare for patients of all ages',
            'services': ['Preventive care', 'Chronic disease management', 'Acute illness treatment', 'Health screenings'],
            'icon': 'ri-heart-pulse-line',
            'billing_challenges': ['Complex coding for multiple conditions', 'Preventive vs. problem-focused visit distinctions', 'Coordination of care documentation'],
            'solutions': ['Specialized family practice coding expertise', 'Preventive service tracking and reminders', 'Chronic care management billing optimization']
        },
        'dermatology': {
            'title': 'Dermatology',
            'description': 'Specialized care for skin, hair, and nail conditions',
            'services': ['Skin cancer screenings', 'Acne treatment', 'Eczema management', 'Cosmetic procedures'],
            'icon': 'ri-user-heart-line',
            'billing_challenges': ['Cosmetic vs. medically necessary procedure distinction', 'Complex coding for biopsies and excisions', 'Multiple procedure reductions'],
            'solutions': ['Dermatology-specific documentation templates', 'Specialized modifier usage training', 'Cosmetic procedure financial protocols']
        },
        'optometry': {
            'title': 'Optometry',
            'description': 'Vision care and eye health services',
            'services': ['Comprehensive eye exams', 'Contact lens fittings', 'Vision therapy', 'Eye disease management'],
            'icon': 'ri-eye-line',
            'billing_challenges': ['Vision vs. medical insurance coordination', 'Refraction billing limitations', 'Special testing documentation requirements'],
            'solutions': ['Vision/medical plan coordination protocols', 'Refraction unbundling compliance', 'Specialized optometry coding expertise']
        },
        'orthopedic': {
            'title': 'Orthopedic',
            'description': 'Treatment for musculoskeletal conditions and injuries',
            'services': ['Joint replacement', 'Fracture care', 'Sports medicine', 'Spine care'],
            'icon': 'ri-body-scan-line',
            'billing_challenges': ['Global period management', 'Complex fracture care coding', 'Workers\' compensation coordination'],
            'solutions': ['Global period tracking systems', 'Orthopedic-specific documentation templates', 'Workers\' comp billing expertise']
        },
        'wound-care': {
            'title': 'Wound Care',
            'description': 'Specialized treatment for chronic and non-healing wounds',
            'services': ['Diabetic ulcer treatment', 'Pressure ulcer management', 'Surgical wound care', 'Hyperbaric oxygen therapy'],
            'icon': 'ri-first-aid-kit-line',
            'billing_challenges': ['Detailed wound measurement documentation', 'Medical necessity for debridement', 'Hyperbaric oxygen therapy authorization'],
            'solutions': ['Wound-specific documentation protocols', 'Specialized wound care coding expertise', 'HBO therapy authorization management']
        },
        'general-surgery': {
            'title': 'General Surgery',
            'description': 'Surgical procedures for various conditions',
            'services': ['Abdominal surgery', 'Hernia repair', 'Gallbladder removal', 'Appendectomy'],
            'icon': 'ri-scissors-line',
            'billing_challenges': ['Global surgical package management', 'Assistant surgeon justification', 'Multiple procedure coding'],
            'solutions': ['Surgical coding expertise', 'Global period tracking and management', 'Operative report optimization']
        }
    }
    
    # Get the details for the requested specialty type
    details = specialty_details.get(specialty_type, {
        'title': 'Specialty',
        'description': 'Information about this specialty',
        'services': [],
        'icon': 'ri-hospital-line',
        'billing_challenges': [],
        'solutions': []
    })
    
    return render_template('specialty.html', 
                           title=details['title'],
                           description=details['description'],
                           services=details['services'],
                           icon=details['icon'],
                           billing_challenges=details['billing_challenges'],
                           solutions=details['solutions'],
                           specialty_type=specialty_type)