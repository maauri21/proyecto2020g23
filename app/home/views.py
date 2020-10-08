from flask import render_template
from flask_login import login_required

from . import home

# En el @ y en la url acordarse de home que es el nombre del blueprint

@home.route('/')
def index():
    return render_template('home/index.html', title="Home")

# vista de admin
@home.route('/paneladmin')
@login_required
def paneladmin():
    return render_template('home/paneladmin.html', title="Panel admin")