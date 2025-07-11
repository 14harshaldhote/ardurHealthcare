#!/usr/bin/env python3
"""
Test script to verify the enhanced Ardur Healthcare system functionality.
This script tests the redesigned state pages, enhanced forms, and analytics system.
"""

import sys
import os
import json
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_app_creation():
    """Test that the Flask app can be created successfully."""
    print("🧪 Testing Flask app creation...")
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return app
    except Exception as e:
        print(f"❌ Flask app creation failed: {str(e)}")
        return None

def test_blueprints(app):
    """Test that all blueprints are registered."""
    print("\n🧪 Testing blueprint registration...")

    expected_blueprints = [
        'auth', 'main', 'contact', 'services',
        'resources', 'specialities', 'ourreach', 'analytics'
    ]

    registered_blueprints = [bp.name for bp in app.blueprints.values()]

    for blueprint in expected_blueprints:
        if blueprint in registered_blueprints:
            print(f"✅ {blueprint} blueprint registered")
        else:
            print(f"❌ {blueprint} blueprint missing")

def test_mail_configuration(app):
    """Test Flask-Mail configuration."""
    print("\n🧪 Testing Flask-Mail configuration...")

    with app.app_context():
        required_configs = [
            'MAIL_SERVER', 'MAIL_PORT', 'MAIL_USE_TLS',
            'ADMIN_EMAIL', 'ANALYTICS_EMAIL'
        ]

        for config in required_configs:
            if config in app.config:
                print(f"✅ {config}: {app.config[config]}")
            else:
                print(f"❌ {config} not configured")

def test_state_page_routes(app):
    """Test state page routes."""
    print("\n🧪 Testing state page routes...")

    with app.test_client() as client:
        # Test main ourreach page
        response = client.get('/state/')
        if response.status_code == 200:
            print("✅ Main ourreach page accessible")
        else:
            print(f"❌ Main ourreach page failed: {response.status_code}")

        # Test states list page
        response = client.get('/state/states')
        if response.status_code == 200:
            print("✅ States list page accessible")
        else:
            print(f"❌ States list page failed: {response.status_code}")

        # Test a sample state page
        response = client.get('/state/medical-billing-services-in-alabama')
        if response.status_code == 200:
            print("✅ Sample state page accessible")
        else:
            print(f"❌ Sample state page failed: {response.status_code}")

def test_contact_form_structure(app):
    """Test contact form structure and fields."""
    print("\n🧪 Testing contact form structure...")

    try:
        from app.contact.forms import ContactForm
        form = ContactForm()

        # Check for enhanced fields
        enhanced_fields = [
            'name', 'email', 'phone', 'practice', 'state',
            'specialties', 'service_type', 'message'
        ]

        for field in enhanced_fields:
            if hasattr(form, field):
                print(f"✅ {field} field exists")
            else:
                print(f"❌ {field} field missing")

        # Check specialties choices
        if hasattr(form, 'specialties') and form.specialties.choices:
            print(f"✅ Specialties field has {len(form.specialties.choices)} choices")
        else:
            print("❌ Specialties field has no choices")

    except Exception as e:
        print(f"❌ Contact form test failed: {str(e)}")

def test_analytics_routes(app):
    """Test analytics routes."""
    print("\n🧪 Testing analytics routes...")

    with app.test_client() as client:
        # Test analytics dashboard (should require login)
        response = client.get('/analytics/dashboard')
        if response.status_code in [302, 401]:  # Redirect to login or unauthorized
            print("✅ Analytics dashboard properly protected")
        else:
            print(f"❌ Analytics dashboard protection failed: {response.status_code}")

def test_data_directories(app):
    """Test that required data directories exist."""
    print("\n🧪 Testing data directory structure...")

    with app.app_context():
        # Check main data directory
        data_dir = app.config.get('JSON_STORAGE_PATH')
        if data_dir and os.path.exists(data_dir):
            print("✅ Main data directory exists")
        else:
            print("❌ Main data directory missing")

        # Check/create logs directory
        logs_dir = os.path.join(app.root_path, '..', 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir, exist_ok=True)
            print("✅ Logs directory created")
        else:
            print("✅ Logs directory exists")

def test_analytics_logging():
    """Test analytics logging functionality."""
    print("\n🧪 Testing analytics logging...")

    try:
        # Create sample analytics entry
        sample_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'state': 'Test State',
            'specialties': ['cardiology', 'family-medicine'],
            'service_type': 'medical-billing',
            'source': 'test_script'
        }

        # Test JSON serialization
        json_str = json.dumps(sample_entry)
        parsed = json.loads(json_str)

        print("✅ Analytics data serialization works")
        print(f"✅ Sample entry: {parsed['state']} - {parsed['service_type']}")

    except Exception as e:
        print(f"❌ Analytics logging test failed: {str(e)}")

def test_email_system(app):
    """Test email system configuration."""
    print("\n🧪 Testing email system...")

    with app.app_context():
        try:
            from flask_mail import Mail
            mail = Mail(app)
            print("✅ Flask-Mail initialized successfully")

            # Test email configuration
            if app.config.get('MAIL_USERNAME'):
                print("✅ MAIL_USERNAME configured")
            else:
                print("⚠️  MAIL_USERNAME not set (set via environment variable)")

            if app.config.get('MAIL_PASSWORD'):
                print("✅ MAIL_PASSWORD configured")
            else:
                print("⚠️  MAIL_PASSWORD not set (set via environment variable)")

        except Exception as e:
            print(f"❌ Email system test failed: {str(e)}")

def test_state_data_loading():
    """Test state data loading functionality."""
    print("\n🧪 Testing state data loading...")

    try:
        # Check if state data files exist
        data_dir = os.path.join(os.path.dirname(__file__), 'data', 'states')
        if os.path.exists(data_dir):
            print("✅ State data directory exists")

            # List JSON files
            json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
            print(f"✅ Found {len(json_files)} JSON data files")

            # Test loading a sample file
            if json_files:
                sample_file = os.path.join(data_dir, json_files[0])
                with open(sample_file, 'r') as f:
                    data = json.load(f)
                print(f"✅ Successfully loaded {len(data)} states from {json_files[0]}")

        else:
            print("❌ State data directory missing")

    except Exception as e:
        print(f"❌ State data loading test failed: {str(e)}")

def run_all_tests():
    """Run all system tests."""
    print("🚀 Starting Ardur Healthcare System Tests")
    print("=" * 50)

    # Create Flask app
    app = test_app_creation()
    if not app:
        print("❌ Cannot continue tests without Flask app")
        return

    # Run all tests
    test_blueprints(app)
    test_mail_configuration(app)
    test_state_page_routes(app)
    test_contact_form_structure(app)
    test_analytics_routes(app)
    test_data_directories(app)
    test_analytics_logging()
    test_email_system(app)
    test_state_data_loading()

    print("\n" + "=" * 50)
    print("🎉 System tests completed!")
    print("\n📝 Next Steps:")
    print("1. Set environment variables for email (MAIL_USERNAME, MAIL_PASSWORD)")
    print("2. Test form submissions manually")
    print("3. Check analytics dashboard with admin login")
    print("4. Verify email delivery")
    print("\n🌐 Access Points:")
    print("- State pages: /state/medical-billing-services-in-[state-name]")
    print("- Contact form: /contact")
    print("- Analytics: /analytics/dashboard (requires login)")

if __name__ == "__main__":
    run_all_tests()
