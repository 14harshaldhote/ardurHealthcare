# app/resources/__init__.py
from flask import Blueprint

# Define the blueprint
resources = Blueprint('resources', __name__, template_folder='templates')

# Import routes AFTER the blueprint is defined.
from . import routes