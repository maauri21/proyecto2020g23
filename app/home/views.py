from flask import render_template, request, url_for, redirect
from flask_login import login_required
from ..models import Configuracion

from . import home

@home.route('/')
def index():
    """
    Pagina principal
    """
    return render_template('home/index.html')

# Vistas de visitantes
@home.before_request
def verificar_mantenimiento():
    config = Configuracion.query.first()
    modo_mantenimiento = config.mantenimiento
    # Si estoy en modo mantenimiento y puse una url distinta a /mantenimiento
    if modo_mantenimiento and request.path != url_for('home.mantenimiento'):
        return redirect(url_for('home.mantenimiento'))

@home.route('/mantenimiento')
def mantenimiento():
    return render_template('home/mantenimiento.html')

# Vistas de visitantes
@home.context_processor
def mostrar_config():
    """
    context_processor se ejecuta antes que se procese la plantilla
    """
    config = Configuracion.query.first()
    return dict(mostrar_config=config)