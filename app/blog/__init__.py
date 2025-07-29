from flask import Blueprint

blog = Blueprint('blog', __name__, url_prefix='/admin/blog')

from . import routes
