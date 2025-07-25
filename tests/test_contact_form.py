import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.contact.forms import ContactForm

class TestContactForm(unittest.TestCase):
    """Comprehensive test suite for the contact form functionality"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after each test method."""
        self.app_context.pop()

    def test_contact_form_get_request(self):
        """Test that the contact form loads correctly on GET request"""
        response = self.client.get('/contact-us')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Connect with Ardur Healthcare', response.data)
        self.assertIn(b'Send us a Message', response.data)

    def test_contact_form_valid_submission(self):
        """Test successful form submission with valid data"""
        with patch('app.contact.routes.threading.Thread') as mock_thread:
            mock_thread_instance = MagicMock()
            mock_thread.return_value = mock_thread_instance

            form_data = {
                'name': 'Dr. John Smith',
                'email': 'john.smith@example.com',
                'phone_country_code': '+1',
                'phone_number': '5551234567',
                'practice': 'Smith Medical Center',
                'state': 'California',
                'specialties': 'Family Practice, Internal Medicine',
                'service_type': 'medical-billing',
                'monthly_insurance': '50000',
                'subject': 'Billing Services Inquiry',
                'message': 'I am interested in your medical billing services for my practice.',
                'privacy_policy_agreement': True
            }

            response = self.client.post('/contact-us', data=form_data, follow_redirects=True)

            # Check for successful submission
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Thank you, Dr. John Smith!', response.data)

            # Verify background thread was started
            mock_thread.assert_called_once()
            mock_thread_instance.start.assert_called_once()

    def test_contact_form_missing_required_fields(self):
        """Test form validation with missing required fields"""
        form_data = {
            'name': 'Dr. John Smith',
            # Missing email
            'phone_number': '5551234567',
            # Missing practice name
            'state': 'California',
            # Missing specialties
            'service_type': 'medical-billing',
            'message': 'Test message',
            'privacy_policy_agreement': True
        }

        response = self.client.post('/contact-us', data=form_data)
        self.assertEqual(response.status_code, 200)

        # Should show validation errors
        self.assertIn(b'Email is required', response.data)
        self.assertIn(b'Practice name is required', response.data)
        self.assertIn(b'Please select at least one specialty', response.data)

    def test_contact_form_invalid_email(self):
        """Test form validation with invalid email format"""
        form_data = {
            'name': 'Dr. John Smith',
            'email': 'invalid-email',
            'phone_number': '5551234567',
            'practice': 'Smith Medical Center',
            'state': 'California',
            'specialties': 'Family Practice',
            'service_type': 'medical-billing',
            'message': 'Test message with sufficient length',
            'privacy_policy_agreement': True
        }

        response = self.client.post('/contact-us', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid email address', response.data)

    def test_contact_form_invalid_phone(self):
        """Test form validation with invalid phone number"""
        form_data = {
            'name': 'Dr. John Smith',
            'email': 'john.smith@example.com',
            'phone_number': '123',  # Too short
            'practice': 'Smith Medical Center',
            'state': 'California',
            'specialties': 'Family Practice',
            'service_type': 'medical-billing',
            'message': 'Test message with sufficient length',
            'privacy_policy_agreement': True
        }

        response = self.client.post('/contact-us', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Phone number must be at least 10 digits', response.data)

    def test_contact_form_empty_specialties(self):
        """Test form validation with empty specialties field"""
        form_data = {
            'name': 'Dr. John Smith',
            'email': 'john.smith@example.com',
            'phone_number': '5551234567',
            'practice': 'Smith Medical Center',
            'state': 'California',
            'specialties': '',  # Empty specialties
            'service_type': 'medical-billing',
            'message': 'Test message with sufficient length',
            'privacy_policy_agreement': True
        }

        response = self.client.post('/contact-us', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please select at least one specialty', response.data)

    def test_contact_form_whitespace_specialties(self):
        """Test form validation with whitespace-only specialties"""
        form_data = {
            'name': 'Dr. John Smith',
            'email': 'john.smith@example.com',
            'phone_number': '5551234567',
            'practice': 'Smith Medical Center',
            'state': 'California',
            'specialties': '   ,  ,   ',  # Only whitespace and commas
            'service_type': 'medical-billing',
            'message': 'Test message with sufficient length',
            'privacy_policy_agreement': True
        }

        response = self.client.post('/contact-us', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please select at least one specialty', response.data)

    def test_contact_form_short_message(self):
        """Test form validation with message too short"""
        form_data = {
            'name': 'Dr. John Smith',
            'email': 'john.smith@example.com',
            'phone_number': '5551234567',
            'practice': 'Smith Medical Center',
            'state': 'California',
            'specialties': 'Family Practice',
            'service_type': 'medical-billing',
            'message': 'Short',  # Too short
            'privacy_policy_agreement': True
        }

        response = self.client.post('/contact-us', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Message must be between 10-1000 characters', response.data)

    def test_contact_form_privacy_policy_not_agreed(self):
        """Test form validation without privacy policy agreement"""
        form_data = {
            'name': 'Dr. John Smith',
            'email': 'john.smith@example.com',
            'phone_number': '5551234567',
            'practice': 'Smith Medical Center',
            'state': 'California',
            'specialties': 'Family Practice',
            'service_type': 'medical-billing',
            'message': 'Test message with sufficient length',
            # privacy_policy_agreement not included (defaults to False)
        }

        response = self.client.post('/contact-us', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You must agree to the Privacy Policy', response.data)

    def test_specialties_api_endpoint(self):
        """Test the specialties API endpoint"""
        response = self.client.get('/api/specialties')
        self.assertEqual(response.status_code, 200)

        # Check that response is JSON
        self.assertEqual(response.content_type, 'application/json')

        # Parse JSON response
        import json
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_specialties_api_with_query(self):
        """Test the specialties API endpoint with search query"""
        response = self.client.get('/api/specialties?q=family')
        self.assertEqual(response.status_code, 200)

        import json
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

        # All returned specialties should contain 'family' (case insensitive)
        for specialty in data:
            self.assertIn('family', specialty.lower())

    def test_contact_form_with_multiple_specialties(self):
        """Test form submission with multiple specialties"""
        with patch('app.contact.routes.threading.Thread') as mock_thread:
            mock_thread_instance = MagicMock()
            mock_thread.return_value = mock_thread_instance

            form_data = {
                'name': 'Dr. Jane Doe',
                'email': 'jane.doe@example.com',
                'phone_number': '5559876543',
                'practice': 'Doe Family Clinic',
                'state': 'Texas',
                'specialties': 'Family Practice, Pediatrics, Internal Medicine, Cardiology',
                'service_type': 'full-service',
                'message': 'I need comprehensive billing services for my multi-specialty practice.',
                'privacy_policy_agreement': True
            }

            response = self.client.post('/contact-us', data=form_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Thank you, Dr. Jane Doe!', response.data)

    def test_contact_form_xss_protection(self):
        """Test form handles potentially malicious input safely"""
        form_data = {
            'name': '<script>alert("xss")</script>Dr. Evil',
            'email': 'evil@example.com',
            'phone_number': '5551234567',
            'practice': '<img src=x onerror=alert("xss")>Evil Practice',
            'state': 'California',
            'specialties': 'Family Practice',
            'service_type': 'medical-billing',
            'message': 'This is a test message with <script>alert("xss")</script> content',
            'privacy_policy_agreement': True
        }

        with patch('app.contact.routes.threading.Thread'):
            response = self.client.post('/contact-us', data=form_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Check that script tags are not executed in the response
            self.assertNotIn(b'<script>', response.data)

    def test_contact_form_sql_injection_protection(self):
        """Test form handles SQL injection attempts"""
        form_data = {
            'name': "'; DROP TABLE users; --",
            'email': 'test@example.com',
            'phone_number': '5551234567',
            'practice': "'; DELETE FROM contacts; --",
            'state': 'California',
            'specialties': 'Family Practice',
            'service_type': 'medical-billing',
            'message': 'This is a test message for SQL injection',
            'privacy_policy_agreement': True
        }

        with patch('app.contact.routes.threading.Thread'):
            # This should not cause any database errors
            response = self.client.post('/contact-us', data=form_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)


class TestContactFormUnit(unittest.TestCase):
    """Unit tests for the ContactForm class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after each test method."""
        self.app_context.pop()

    def test_valid_form_data(self):
        """Test ContactForm with valid data"""
        with self.app.test_request_context():
            form_data = {
                'name': 'Dr. Test',
                'email': 'test@example.com',
                'phone_number': '5551234567',
                'practice': 'Test Practice',
                'state': 'California',
                'specialties': 'Family Practice, Internal Medicine',
                'service_type': 'medical-billing',
                'message': 'This is a test message with sufficient length',
                'privacy_policy_agreement': True
            }
            form = ContactForm(data=form_data)
            self.assertTrue(form.validate())

    def test_specialty_validation_empty(self):
        """Test specialty validation with empty input"""
        with self.app.test_request_context():
            from app.contact.forms import validate_specialties
            from wtforms import ValidationError

            # Mock field with empty data
            field = MagicMock()
            field.data = ''

            with self.assertRaises(ValidationError) as context:
                validate_specialties(None, field)

            self.assertIn('Please select at least one specialty', str(context.exception))

    def test_specialty_validation_whitespace(self):
        """Test specialty validation with whitespace only"""
        with self.app.test_request_context():
            from app.contact.forms import validate_specialties
            from wtforms import ValidationError

            field = MagicMock()
            field.data = '   ,  ,   '  # Only whitespace and commas

            with self.assertRaises(ValidationError):
                validate_specialties(None, field)

    def test_specialty_validation_valid(self):
        """Test specialty validation with valid input"""
        with self.app.test_request_context():
            from app.contact.forms import validate_specialties

            field = MagicMock()
            field.data = 'Family Practice, Internal Medicine'

            # Should not raise ValidationError
            try:
                validate_specialties(None, field)
            except Exception as e:
                self.fail(f"validate_specialties raised {type(e).__name__} unexpectedly: {e}")

    def test_phone_number_validation(self):
        """Test phone number custom validation"""
        with self.app.test_request_context():
            form_data = {
                'name': 'Dr. Test',
                'email': 'test@example.com',
                'phone_number': '123',  # Too short
                'practice': 'Test Practice',
                'state': 'California',
                'specialties': 'Family Practice',
                'service_type': 'medical-billing',
                'message': 'This is a test message with sufficient length',
                'privacy_policy_agreement': True
            }
            form = ContactForm(data=form_data)
            self.assertFalse(form.validate())
            self.assertIn('Phone number must be at least 10 digits', form.phone_number.errors)


if __name__ == '__main__':
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestContactForm))
    suite.addTests(loader.loadTestsFromTestCase(TestContactFormUnit))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)
