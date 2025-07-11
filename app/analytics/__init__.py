from flask import Blueprint

analytics = Blueprint('analytics', __name__, url_prefix='/analytics')

from . import routes  # noqa: F401
