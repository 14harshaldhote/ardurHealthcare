from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates') # Or just 'templates'

from . import routes