from flask import Blueprint

# inicializo e importo vistas
auth = Blueprint('auth', __name__)

from . import views