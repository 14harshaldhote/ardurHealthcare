# app/contact/routes.py
from flask import render_template, flash, redirect, url_for, current_app
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
@contact.route('/contact', methods=['GET', 'POST'])
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
            'timestamp': datetime.utcnow().isoformat()
        }

        try:
            # Send admin email with complete form data
            send_admin_email(form_data)

            # Send analytics email with non-personal data only
            send_analytics_email(form_data)

            # Log data for internal analytics
            log_form_submission(form_data)

            # Use Flask's flash system to show a success message to the user.
            flash(f'Thank you, {name}! Your message has been sent successfully. We will contact you within 24 hours.', 'success')

        except Exception as e:
            current_app.logger.error(f"Error processing contact form: {str(e)}")
            flash('There was an error sending your message. Please try again or call us directly at (214) 800-6161.', 'error')

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

        # Format specialties for better readability
        specialties_text = ', '.join(form_data['specialties']) if form_data['specialties'] else 'Not specified'

        # Create email content
        email_body = f"""
New Contact Form Submission - {form_data['timestamp']}

CONTACT INFORMATION:
Name: {form_data['name']}
Email: {form_data['email']}
Phone: {form_data['phone']}
Practice: {form_data['practice_name'] or 'Not specified'}
State: {form_data['state']}

SERVICE DETAILS:
Specialties: {specialties_text}
Service Type: {form_data['service_type'] or 'Not specified'}

MESSAGE:
{form_data['message']}

---
This message was sent from the Ardur Healthcare contact form.
        """

        # Create and send message
        msg = Message(
            subject=f"New Contact Form: {form_data['subject']}",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@ardurhealthcare.com'),
            recipients=[current_app.config.get('ADMIN_EMAIL', 'admin@ardurhealthcare.com')],
            body=email_body
        )

        mail.send(msg)
        current_app.logger.info(f"Admin email sent successfully for {form_data['name']}")

    except Exception as e:
        current_app.logger.error(f"Error sending admin email: {str(e)}")
        raise


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
