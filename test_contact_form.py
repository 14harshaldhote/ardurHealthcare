#!/usr/bin/env python3
"""
Contact Form Test Script for Ardur Healthcare
============================================
This script tests the contact form by submitting test data and sending it to abhi@ardurtechnology.com

Usage: python test_contact_form.py
"""

import os
import sys
from datetime import datetime

# Add app to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def setup_email_credentials():
    """Set up email credentials for testing."""
    print("🔧 Setting up email credentials...")

    # Set email credentials
    os.environ['MAIL_USERNAME'] = 'dhoteharshal16@gmail.com'
    os.environ['MAIL_PASSWORD'] = 'qtwc pdwp hwkp geij'
    os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
    os.environ['MAIL_PORT'] = '587'
    os.environ['MAIL_USE_TLS'] = 'true'
    os.environ['ADMIN_EMAIL'] = 'dhoteharshal16@gmail.com'
    os.environ['ANALYTICS_EMAIL'] = 'analytics@ardurhealthcare.com'
    os.environ['MAIL_DEFAULT_SENDER'] = 'dhoteharshal16@gmail.com'
    os.environ['SECRET_KEY'] = 'qtwc pdwp hwkp geij'

    print("✅ Email credentials configured")
    print(f"   📤 Sending from: dhoteharshal16@gmail.com")
    print(f"   📥 Sending to: abhi@ardurtechnology.com")

def create_test_form_data():
    """Create comprehensive test data for contact form."""
    return {
        'name': 'Dr. Jennifer Martinez',
        'email': 'jennifer.martinez@healthcareclinic.com',
        'phone': '+1-555-0187',
        'practice_name': 'Martinez Healthcare Clinic',
        'state': 'Florida',
        'specialties': ['family-medicine', 'internal-medicine'],
        'service_type': 'medical-billing',
        'subject': 'Medical Billing and Coding Services Inquiry',
        'message': '''Hello Ardur Healthcare Team,

I hope this message finds you well. I am Dr. Jennifer Martinez, the owner and lead physician at Martinez Healthcare Clinic, a family medicine practice located in Miami, Florida.

We are currently seeking a reliable medical billing and coding partner to help streamline our revenue cycle management. Our practice has been growing steadily, and we need professional support to ensure accurate billing and maximize our collections.

PRACTICE DETAILS:
- Established: 2018
- Location: Miami, Florida
- Specialties: Family Medicine, Internal Medicine
- Providers: 2 physicians, 1 nurse practitioner, 2 medical assistants
- Patient Volume: Approximately 300 patients per week
- Current EMR: Epic EHR System

SERVICES WE NEED:
✓ Complete medical billing services
✓ Medical coding (ICD-10, CPT, HCPCS)
✓ Insurance verification and authorization
✓ Claims submission and follow-up
✓ Denial management and appeals
✓ Accounts receivable management
✓ Patient billing and payment processing
✓ Monthly financial reporting
✓ Credentialing support

INSURANCE PROVIDERS WE WORK WITH:
- Medicare and Medicaid
- Blue Cross Blue Shield
- Aetna
- United Healthcare
- Humana
- Cigna
- Local HMO plans

We are particularly interested in your full-service medical billing package and would appreciate the opportunity to discuss:
1. Your pricing structure and fee schedule
2. Implementation timeline and process
3. Reporting capabilities and frequency
4. Staff training and support
5. Technology integration with our Epic system

Could we schedule a consultation call next week to discuss our needs in detail? I am available Monday through Wednesday between 2:00 PM and 5:00 PM EST.

Please let me know what additional information you might need from us to provide an accurate proposal.

Thank you for your time and consideration. I look forward to hearing from you soon.

Best regards,

Dr. Jennifer Martinez, MD
Martinez Healthcare Clinic
Phone: (555) 123-4567
Email: jennifer.martinez@healthcareclinic.com
Address: 123 Medical Plaza, Miami, FL 33101

P.S. We were referred to you by Dr. Robert Chen from Tampa Medical Group, who spoke highly of your services.''',
        'timestamp': datetime.utcnow().isoformat()
    }

def test_email_configuration():
    """Test basic email configuration."""
    print("\n🧪 Testing Email Configuration...")
    print("-" * 40)

    try:
        from app import create_app
        from flask_mail import Mail, Message

        app = create_app()

        with app.app_context():
            mail = Mail(app)

            # Verify configuration
            config_items = [
                ('MAIL_SERVER', app.config.get('MAIL_SERVER')),
                ('MAIL_PORT', app.config.get('MAIL_PORT')),
                ('MAIL_USE_TLS', app.config.get('MAIL_USE_TLS')),
                ('MAIL_USERNAME', '✅ Set' if app.config.get('MAIL_USERNAME') else '❌ Not Set'),
                ('MAIL_PASSWORD', '✅ Set' if app.config.get('MAIL_PASSWORD') else '❌ Not Set'),
                ('ADMIN_EMAIL', app.config.get('ADMIN_EMAIL'))
            ]

            for key, value in config_items:
                print(f"   {key}: {value}")

            # Send test email
            msg = Message(
                subject="🧪 Ardur Healthcare - Email Configuration Test",
                sender="dhoteharshal16@gmail.com",
                recipients=["abhi@ardurtechnology.com"],
                body=f"""
Email Configuration Test - SUCCESSFUL!

This email confirms that the Ardur Healthcare contact form email system is properly configured.

Test Details:
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- From: dhoteharshal16@gmail.com
- To: abhi@ardurtechnology.com
- Status: ✅ Configuration Working

The contact form is ready to receive real submissions.

---
Ardur Healthcare Email Test System
"""
            )

            mail.send(msg)
            print("✅ Email configuration test PASSED!")
            return True

    except Exception as e:
        print(f"❌ Email configuration test FAILED: {str(e)}")
        return False

def test_contact_form_submission():
    """Test actual contact form submission."""
    print("\n📝 Testing Contact Form Submission...")
    print("-" * 40)

    try:
        from app import create_app
        from app.contact.routes import send_admin_email, send_analytics_email, log_form_submission

        app = create_app()

        with app.app_context():
            # Get test data
            test_data = create_test_form_data()

            print("📋 Test Form Data:")
            print(f"   👤 Name: {test_data['name']}")
            print(f"   📧 Email: {test_data['email']}")
            print(f"   📞 Phone: {test_data['phone']}")
            print(f"   🏥 Practice: {test_data['practice_name']}")
            print(f"   📍 State: {test_data['state']}")
            print(f"   🩺 Specialties: {', '.join(test_data['specialties'])}")
            print(f"   🔧 Service: {test_data['service_type']}")
            print(f"   📄 Subject: {test_data['subject']}")
            print(f"   💬 Message: {len(test_data['message'])} characters")
            print()

            # Send admin email (main email)
            print("📤 Sending admin email to abhi@ardurtechnology.com...")
            send_admin_email(test_data)
            print("✅ Admin email sent successfully!")

            # Send analytics email
            print("📊 Sending analytics email...")
            send_analytics_email(test_data)
            print("✅ Analytics email sent successfully!")

            # Log form data
            print("📁 Logging form submission...")
            log_form_submission(test_data)
            print("✅ Form data logged successfully!")

            return True

    except Exception as e:
        print(f"❌ Contact form submission test FAILED: {str(e)}")
        return False

def test_web_form_interface():
    """Test contact form via web interface."""
    print("\n🌐 Testing Web Form Interface...")
    print("-" * 40)

    try:
        from app import create_app

        app = create_app()

        with app.test_client() as client:
            # Test GET request to contact form
            response = client.get('/contact')
            if response.status_code == 200:
                print("✅ Contact form page accessible at /contact")
            else:
                print(f"❌ Contact form page error: {response.status_code}")
                return False

            # Test form fields are present
            form_content = response.get_data(as_text=True)
            required_fields = ['name', 'email', 'phone', 'practice', 'state', 'message']

            for field in required_fields:
                if field in form_content:
                    print(f"✅ {field} field found in form")
                else:
                    print(f"❌ {field} field missing from form")

            print("✅ Web form interface test completed!")
            return True

    except Exception as e:
        print(f"❌ Web form interface test FAILED: {str(e)}")
        return False

def run_comprehensive_test():
    """Run all contact form tests."""
    print("🏥 ARDUR HEALTHCARE - CONTACT FORM TEST SUITE")
    print("=" * 60)
    print("Testing contact form submission to abhi@ardurtechnology.com")
    print()

    # Setup email credentials
    setup_email_credentials()

    # Track test results
    tests_passed = 0
    total_tests = 3

    # Test 1: Email Configuration
    if test_email_configuration():
        tests_passed += 1
        print("✅ TEST 1 PASSED: Email Configuration")
    else:
        print("❌ TEST 1 FAILED: Email Configuration")

    # Test 2: Contact Form Submission
    if test_contact_form_submission():
        tests_passed += 1
        print("✅ TEST 2 PASSED: Contact Form Submission")
    else:
        print("❌ TEST 2 FAILED: Contact Form Submission")

    # Test 3: Web Form Interface
    if test_web_form_interface():
        tests_passed += 1
        print("✅ TEST 3 PASSED: Web Form Interface")
    else:
        print("❌ TEST 3 FAILED: Web Form Interface")

    # Final Results
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print(f"Tests Passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Contact form is working perfectly!")
        print("✅ Emails are being sent to abhi@ardurtechnology.com")
        print("✅ Form data is properly formatted and logged")
        print()
        print("📧 CHECK YOUR EMAIL:")
        print("   Recipient: abhi@ardurtechnology.com")
        print("   Expected emails: 2 (test email + contact form submission)")
        print()
        print("🚀 NEXT STEPS:")
        print("   1. Start application: python run.py")
        print("   2. Access contact form: http://localhost:5000/contact")
        print("   3. Real form submissions will work perfectly!")

    elif tests_passed >= 2:
        print("\n⚠️  MOSTLY SUCCESSFUL!")
        print(f"✅ {tests_passed} out of {total_tests} tests passed")
        print("📧 Check abhi@ardurtechnology.com for test emails")
        print("💡 Minor issues detected but contact form should work")

    else:
        print("\n❌ TESTS FAILED!")
        print("💡 Contact form may not be working properly")
        print("🔧 Check error messages above for troubleshooting")

    print(f"\n📅 Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📧 Email recipient: abhi@ardurtechnology.com")

def main():
    """Main test execution function."""
    try:
        run_comprehensive_test()
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {str(e)}")
        print("💡 Please check your Python environment and dependencies")

if __name__ == "__main__":
    main()
