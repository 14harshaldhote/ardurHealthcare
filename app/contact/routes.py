# app/contact/routes.py
from flask import render_template, request, flash, redirect, url_for
# Import the 'contact' blueprint instance from its __init__.py file
from . import contact
# Import your ContactForm from the forms.py file within the same 'contact' package
from .forms import ContactForm


# Define the route for the contact page.
# This route will handle both GET requests (to display the form)
# and POST requests (to process the form submission).
# The endpoint for this route will be 'contact.contact'.
@contact.route('/contact', methods=['GET', 'POST'])
def contact():
    # Create an instance of the ContactForm.
    # Flask-WTF will automatically populate it with submitted data on POST requests.
    form = ContactForm()

    # Check if the form was submitted via POST and if all validators passed.
    if form.validate_on_submit():
        # Retrieve data from the form fields.
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        # --- In a real application, you would perform actions here, e.g.: ---
        # 1. Save the message to a database.
        #    e.g., db.session.add(ContactMessage(name=name, email=email, ...))
        #    db.session.commit()
        # 2. Send an email with the contact message.
        #    e.g., send_email(subject, sender=email, recipients=['your_email@example.com'], body=message)
        # 3. Log the message.
        print(f"New contact message from {name} ({email}) - Subject: {subject}\nMessage: {message}")

        # Use Flask's flash system to show a success message to the user.
        # 'success' is a category that can be used for styling in the template.
        flash(f'Thank you, {name}! Your message has been sent successfully.', 'success')

        # Redirect the user to the same contact page after successful submission.
        # This prevents the "Are you sure you want to resubmit the form?" warning
        # if the user refreshes the page.
        # url_for('contact.contact') builds the URL for the route named 'contact' within the 'contact' blueprint.
        return redirect(url_for('contact.contact'))

    # If the request is GET (initial load) or form validation failed (on POST),
    # render the contact_form.html template.
    # The 'form' object is passed to the template so Jinja can render the form fields.
    return render_template('contact_form.html', form=form)
