from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='../templates')

import app.admin.views
