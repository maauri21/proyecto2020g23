from flask import render_template
from flask_login import login_required

from . import home

# En el @ y en la url acordarse de home que es el nombre del blueprint

@home.route('/')
def index():
<<<<<<< HEAD
    return render_template('home/index.html', title="Home")

# vista de admin
@home.route('/paneladmin')
@login_required
def paneladmin():
    return render_template('home/paneladmin.html', title="Panel admin")
=======
    return render_template('home/index.html', title="Welcome")
>>>>>>> 5a4286af0679cfdf1e5113bfd0b233c880b1826d
