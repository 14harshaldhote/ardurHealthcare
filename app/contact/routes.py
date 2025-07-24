# app/contact/routes.py
from flask import render_template, flash, redirect, url_for, current_app, jsonify, request
from flask_mail import Mail, Message
from datetime import datetime
import json
import os
# Import the 'contact' blueprint instance from its __init__.py file
from . import contact
# Import your ContactForm from the forms.py file within the same 'contact' package
from .forms import ContactForm


# Define the route for the contact page.
# This route will handle both GET requests (to display the form)
# and POST requests (to process the form submission).
# The endpoint for this route will be 'contact.contact'.
@contact.route('/contact-us', methods=['GET', 'POST'])
def contact_form():
    # Create an instance of the ContactForm.
    # Flask-WTF will automatically populate it with submitted data on POST requests.
    form = ContactForm()

    # Check if the form was submitted via POST and if all validators passed.
    if form.validate_on_submit():
        # Retrieve data from the form fields.
        name = form.name.data
        email = form.email.data
        phone = form.phone.data if hasattr(form, 'phone') and form.phone.data else form.phone_number.data
        practice = getattr(form, 'practice', None)
        practice_name = practice.data if practice else None
        state = form.state.data
        specialties = form.specialties.data if hasattr(form, 'specialties') else []
        service_type = getattr(form, 'service_type', None)
        service_type_value = service_type.data if service_type else None
        subject = form.subject.data if form.subject.data else f"Contact Form - {service_type_value or 'General Inquiry'}"
        message = form.message.data
        privacy_policy_agreement = form.privacy_policy_agreement.data

        # Prepare form data for processing
        form_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'practice_name': practice_name,
            'state': state,
            'specialties': specialties,
            'service_type': service_type_value,
            'subject': subject,
            'message': message,
            'privacy_policy_agreement': privacy_policy_agreement,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Track success of different operations
        admin_email_sent = False
        analytics_email_sent = False
        data_logged = False

        try:
            # Send admin email with complete form data (most important)
            current_app.logger.info(f"Attempting to send admin email for {name} ({email})")
            send_admin_email(form_data)
            admin_email_sent = True
            current_app.logger.info(f"✅ Admin email sent successfully to {current_app.config.get('ADMIN_EMAIL')}")

        except Exception as e:
            current_app.logger.error(f"❌ Failed to send admin email: {str(e)}")
            # Continue processing even if admin email fails

        try:
            # Send analytics email with non-personal data only
            send_analytics_email(form_data)
            analytics_email_sent = True
            current_app.logger.info("✅ Analytics email sent successfully")

        except Exception as e:
            current_app.logger.error(f"❌ Failed to send analytics email: {str(e)}")
            # Continue processing even if analytics email fails

        try:
            # Log data for internal analytics
            log_form_submission(form_data)
            data_logged = True
            current_app.logger.info("✅ Form data logged successfully")

        except Exception as e:
            current_app.logger.error(f"❌ Failed to log form data: {str(e)}")

        # Provide feedback based on what succeeded
        if admin_email_sent:
            flash(f'Thank you, {name}! Your message has been sent successfully to our team. We will contact you within 24 hours.', 'success')
            current_app.logger.info(f"✅ Contact form processed successfully for {name} ({email})")
        else:
            flash(f'Thank you, {name}! Your message has been received and logged. Due to a technical issue with email delivery, please also call us at (214) 800-6161 to ensure we received your message.', 'warning')
            current_app.logger.warning(f"⚠️ Contact form processed with email delivery issues for {name} ({email})")

        # Redirect the user to the same contact page after successful submission.
        return redirect(url_for('contact.contact_form'))

    # If the request is GET (initial load) or form validation failed (on POST),
    # render the contact_form.html template.
    # The 'form' object is passed to the template so Jinja can render the form fields.
    return render_template('contact_form.html', form=form)


def send_admin_email(form_data):
    """Send complete form data to admin email"""
    try:
        # Initialize Flask-Mail if not already done
        mail = Mail(current_app)

        # Check if email configuration is available
        if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
            error_msg = "Email credentials not configured. Set MAIL_USERNAME and MAIL_PASSWORD environment variables."
            current_app.logger.error(error_msg)
            raise Exception(error_msg)

        # Format specialties for better readability
        specialties_text = ', '.join(form_data['specialties']) if form_data['specialties'] else 'Not specified'

        # Create enhanced email content
        email_body = f"""
🏥 NEW CONTACT FORM SUBMISSION
========================================

📅 Submitted: {form_data['timestamp']}

👤 CONTACT INFORMATION:
• Name: {form_data['name']}
• Email: {form_data['email']}
• Phone: {form_data['phone']}
• Practice: {form_data['practice_name'] or 'Not specified'}
• State: {form_data['state']}

💼 SERVICE DETAILS:
• Specialties: {specialties_text}
• Service Type: {form_data['service_type'] or 'Not specified'}

💬 MESSAGE:
{form_data['message']}

✅ PRIVACY POLICY AGREEMENT: {'Agreed' if form_data['privacy_policy_agreement'] else 'Not Agreed'}

========================================
📧 Reply directly to this email to respond to {form_data['name']}
📞 Or call them at {form_data['phone']}

This message was sent from the Ardur Healthcare contact form.
Generated: {form_data['timestamp']}
        """

        # Get recipient email with fallback
        admin_email = current_app.config.get('ADMIN_EMAIL', 'abhi@ardurtechnology.com')
        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', current_app.config.get('MAIL_USERNAME'))

        # Create and send message
        msg = Message(
            subject=f"🏥 New Contact: {form_data['name']} - {form_data['service_type'] or 'General Inquiry'}",
            sender=sender_email,
            recipients=[admin_email],
            reply_to=form_data['email'],  # Allow direct reply to customer
            body=email_body
        )

        current_app.logger.info(f"Sending email from {sender_email} to {admin_email}")
        mail.send(msg)
        current_app.logger.info(f"✅ Admin email sent successfully to {admin_email} for {form_data['name']}")

    except Exception as e:
        error_details = f"Error sending admin email: {str(e)}"
        current_app.logger.error(error_details)

        # Log email configuration for debugging
        current_app.logger.error(f"Email config - Server: {current_app.config.get('MAIL_SERVER')}, "
                                f"Port: {current_app.config.get('MAIL_PORT')}, "
                                f"Username: {'SET' if current_app.config.get('MAIL_USERNAME') else 'NOT SET'}, "
                                f"Password: {'SET' if current_app.config.get('MAIL_PASSWORD') else 'NOT SET'}")
        raise Exception(error_details)


def send_analytics_email(form_data):
    """Send non-personal data to analytics email"""
    try:
        # Initialize Flask-Mail if not already done
        mail = Mail(current_app)

        # Format specialties for better readability
        specialties_text = ', '.join(form_data['specialties']) if form_data['specialties'] else 'Not specified'

        # Create analytics email content (no personal info)
        analytics_body = f"""
New Form Submission Analytics - {form_data['timestamp']}

ANALYTICS DATA:
State: {form_data['state']}
Specialties: {specialties_text}
Service Type: {form_data['service_type'] or 'Not specified'}

SUMMARY:
This submission represents interest in {form_data['service_type'] or 'general services'}
from a {specialties_text.lower()} practice in {form_data['state']}.

---
This is anonymized analytics data from Ardur Healthcare contact forms.
        """

        # Create and send message
        msg = Message(
            subject=f"Analytics: {form_data['state']} - {form_data['service_type'] or 'General'}",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@ardurhealthcare.com'),
            recipients=[current_app.config.get('ANALYTICS_EMAIL', 'analytics@ardurhealthcare.com')],
            body=analytics_body
        )

        mail.send(msg)
        current_app.logger.info(f"Analytics email sent successfully for {form_data['state']} submission")

    except Exception as e:
        current_app.logger.error(f"Error sending analytics email: {str(e)}")
        raise


def log_form_submission(form_data):
    """Log form submission data for internal analytics (excluding personal info)"""
    try:
        # Create analytics log entry
        analytics_entry = {
            'timestamp': form_data['timestamp'],
            'state': form_data['state'],
            'specialties': form_data['specialties'],
            'service_type': form_data['service_type'],
            'source': 'contact_form'
        }

        # Ensure logs directory exists
        logs_dir = os.path.join(current_app.root_path, '..', 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        # Create log file path
        log_file = os.path.join(logs_dir, 'analytics_log.json')

        # Read existing logs or create new list
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        # Add new entry
        logs.append(analytics_entry)

        # Keep only last 1000 entries to prevent file from growing too large
        if len(logs) > 1000:
            logs = logs[-1000:]

        # Write back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

        current_app.logger.info(f"Analytics data logged for {form_data['state']} submission")

    except Exception as e:
        current_app.logger.error(f"Error logging analytics data: {str(e)}")
        # Don't raise here - logging failure shouldn't break the form submission


def load_specialty_data():
    """Load specialty data from JSON file"""
    try:
        json_path = os.path.join(current_app.root_path, '..', 'data', 'specialty', 'specialty_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('services', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@contact.route('/api/specialties')
def api_specialties():
    """API endpoint to get all specialties for dynamic search"""
    try:
        # Get specialties from JSON data
        specialties = load_specialty_data()
        json_specialty_names = []
        for s in specialties:
            clean_name = s['specialty'].replace(' Billing Services', '').strip()
            json_specialty_names.append(clean_name)

        # Additional services not in JSON
        additional_services = [
            "Allergy and Immunology",
            "Ambulatory Surgical Center",
            "Anesthesia",
            "Behavioral Health",
            "Cardiology",
            "Chiropractic",
            "Clinical Psychology",
            "Dental",
            "Dermatology",
            "Durable Medical Equipment (DME)",
            "Emergency Room",
            "Endocrinology",
            "Family Practice",
            "Gastroenterology",
            "General Surgery",
            "Home Health",
            "Hospice",
            "Internal Medicine",
            "Laboratory",
            "Massage Therapy",
            "Mental Health",
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
            "Physical Therapy",
            "Plastic Surgery",
            "Podiatry",
            "Primary Care",
            "Pulmonology",
            "Radiation Oncology",
            "Radiology",
            "Rheumatology",
            "Skilled Nursing Facility (SNF)",
            "Sleep Disorder",
            "Sports Medicine",
            "Urgent Care",
            "Urology",
            "Wound Care"
        ]

        # Combine and remove duplicates
        all_specialties = []
        seen = set()

        for name in json_specialty_names + additional_services:
            if name not in seen:
                all_specialties.append(name)
                seen.add(name)

        # Sort alphabetically
        all_specialties = sorted(all_specialties)

        # Filter based on search query if provided
        query = request.args.get('q', '').lower()
        if query:
            filtered_specialties = [s for s in all_specialties if query in s.lower()]
            return jsonify(filtered_specialties[:10])  # Limit to 10 results

        return jsonify(all_specialties)

    except Exception as e:
        current_app.logger.error(f"Error loading specialties: {str(e)}")
        return jsonify([]), 500
