from flask import Blueprint

# inicializo e importo vistas
home = Blueprint('home', __name__)

from . import views