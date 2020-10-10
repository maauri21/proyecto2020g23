from flask import render_template
from flask_login import login_required

from . import home

@home.route('/')
def index():
    """
    Pagina principal
    """
    return render_template('home/index.html')