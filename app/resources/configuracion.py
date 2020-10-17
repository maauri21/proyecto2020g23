from flask import render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.forms.editarsistema import EditarConfigForm
from app.models.configuracion import Configuracion
from app.helpers.permisos import check_permiso
from app.db import db

def mantenimiento():
    return render_template('mantenimiento.html')

@login_required
def editar_configuracion():
    """
    Editar configuracion
    """

    if not check_permiso(current_user, 'config_index'):
        abort(401)
    
    config = Configuracion.buscar_config()
    form = EditarConfigForm()
    if form.validate_on_submit():
        config.titulo = form.titulo.data
        config.descripcion = form.descripcion.data
        config.email = form.email.data
        config.cantPaginacion = form.cantPaginacion.data
        config.mantenimiento = form.mantenimiento.data
        Configuracion.commit()
        flash('Configuración modificada')

        # Redirección al panel de configuracion
        return redirect(url_for('panel_config'))

    
    form.titulo.data = config.titulo
    form.descripcion.data = config.descripcion
    form.email.data = config.email
    form.cantPaginacion.data = config.cantPaginacion
    form.mantenimiento.data = config.mantenimiento
    return render_template('config/panelconfig.html',
                            form=form)