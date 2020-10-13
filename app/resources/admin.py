from flask import render_template
from flask_login import login_required

from app.models.configuracion import Configuracion
from . import app

@login_required
def panel_admin():
    """
    Panel de configuración del admin
    """
    config = Configuracion.query.first()
    return render_template('admin/paneladmin.html', config=config)