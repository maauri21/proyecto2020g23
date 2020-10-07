from flask import Blueprint

# inicializo e importo vistas
admin = Blueprint('admin', __name__)

from . import views