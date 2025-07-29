from flask import Blueprint

crm = Blueprint('crm', __name__, url_prefix='/crm')

from . import routes
