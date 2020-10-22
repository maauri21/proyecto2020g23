from flask import flash, redirect, render_template, url_for, session, request, abort
from flask_login import login_required, current_user

from app.forms.centro import CentroForm
from app.forms.buscarcentro import BuscarCentroForm
from app.db import db
from app.models.centro import Centro
from app.models.configuracion import Configuracion
from app.helpers.permisos import check_permiso

from werkzeug.utils import secure_filename
import os
from flask import current_app as app

@login_required
def buscar_centros():
    """
    Listar centros
    """

    if not check_permiso(current_user, 'centro_index'):
        abort(401)

    config = Configuracion.query.first()
    form = BuscarCentroForm(formdata=request.args)
    buscar = form.data['search']
    estado = form.data['select']
    pag = int(request.args.get('num_pag', 1))

    if form.data['select'] != 'Todos':
        centros = Centro.query.filter(Centro.estado.contains(estado)).filter(Centro.nombre.contains(buscar)).paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
    else:
        centros = Centro.query.filter(Centro.nombre.contains(buscar)).paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
    return render_template('centros/centros.html',
                            form=form,
                            centros=centros)

@login_required
def agregar_centro():
    """
    Agregar centro
    """
    agregar_centro = True

    if not check_permiso(current_user, 'centro_new'):
        abort(401)

    form = CentroForm()
    if form.validate_on_submit():
        file = form.protocolo.data
        filename = secure_filename(file.filename)
        nombreArchivo = None
        if file:
            # Por si suben 2 archivos con el mismo nombre, lo renombro poniendole el nombre del centro 1ro
            nombreArchivo = form.nombre.data+'_'+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreArchivo))
        centro = Centro(nombre=form.nombre.data,
                            direccion=form.direccion.data,
                            telefono=form.telefono.data,
                            apertura=form.apertura.data,
                            cierre=form.cierre.data,
                            tipo=form.tipo.data,
                            municipio=form.municipio.data,
                            web=form.web.data,
                            email=form.email.data,
                            estado='Aceptado',
                            protocolo = nombreArchivo,
                            coordenadas=form.coordenadas.data)

        Centro.agregar(centro)
        Centro.commit()
        flash('Centro agregado')

        # Redirección al listado dsp de agregar
        return redirect(url_for('buscar_centros'))

    return render_template('centros/centro.html',
                           agregar_centro=agregar_centro,
                           form=form)