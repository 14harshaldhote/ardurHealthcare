# app/specialities/__init__.py
from flask import Blueprint

# Define the blueprint
specialities = Blueprint('specialities', __name__, template_folder='templates')

# Import routes AFTER the blueprint is defined.
from . import routes  # noqa: F401
