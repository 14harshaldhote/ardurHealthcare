# app/contact/__init__.py
from flask import Blueprint

# Define the blueprint
# The template_folder='templates' is explicit but 'templates' is the default and often not needed.
contact = Blueprint('contact', __name__, template_folder='templates')

# Import routes AFTER the blueprint is defined.
# This ensures that 'contact' blueprint object is available when routes.py is executed.
from . import routes
