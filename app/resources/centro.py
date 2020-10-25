from flask import flash, redirect, render_template, url_for, session, request, abort, jsonify
from flask_login import login_required, current_user

from app.forms.centro import CentroForm
from app.forms.editarcentro import EditarCentroForm
from app.forms.validar_centro import ValidarCentroForm
from app.forms.buscarcentro import BuscarCentroForm
from app.db import db
from app.models.centro import Centro, centro_schema, centros_schema
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


@login_required
def editar_centro(id):
    """
    Editar centro
    """

    if not check_permiso(current_user, 'centro_update'):
        abort(401)

    agregar_centro = False
    centro = Centro.buscar(id)
    form = EditarCentroForm()
    if form.validate_on_submit():
        centro.nombre = form.nombre.data
        centro.direccion = form.direccion.data
        centro.telefono = form.telefono.data
        centro.apertura = form.apertura.data
        centro.cierre = form.cierre.data
        centro.tipo = form.tipo.data
        centro.municipio = form.municipio.data
        centro.web = form.web.data
        centro.email = form.email.data
        centro.coordenadas = form.coordenadas.data
        Centro.commit()
        flash('Centro modificado')

        # Redirección al listado dsp de editar
        return redirect(url_for('buscar_centros'))

    session['idCentro'] = id
    form.nombre.data = centro.nombre
    form.direccion.data = centro.direccion
    form.telefono.data = centro.telefono
    form.apertura.data = centro.apertura
    form.cierre.data = centro.cierre
    form.tipo.data = centro.tipo
    form.municipio.data = centro.municipio
    form.web.data = centro.web
    form.email.data = centro.email
    form.coordenadas.data = centro.coordenadas
    return render_template('centros/centro.html',
                            agregar_centro=agregar_centro, form=form)

@login_required
def borrar_centro(id):
    """
    Borrar centro
    """

    if not check_permiso(current_user, 'centro_destroy'):
        abort(401)

    centro = Centro.buscar(id)
    Centro.eliminar(centro)
    Centro.commit()
    flash('Centro borrado')
    # Redirección al listado dsp de borrar
    return redirect(url_for('buscar_centros'))

@login_required
def validar_centro(id):
    """
    Validar centro
    """

    if not check_permiso(current_user, 'centro_validate'):
        abort(401)

    centro = Centro.buscar(id)
    form = ValidarCentroForm()
    if form.validate_on_submit():
        if form.aceptar.data:
            centro.estado = 'Aceptado'
        elif form.rechazar.data:
            centro.estado = 'Rechazado'
        Centro.commit()
        flash('Centro validado')
        return redirect(url_for('buscar_centros'))

    session['idCentro'] = id
    form.nombre.data = centro.nombre
    form.direccion.data = centro.direccion
    form.telefono.data = centro.telefono
    form.apertura.data = centro.apertura
    form.cierre.data = centro.cierre
    form.tipo.data = centro.tipo
    form.municipio.data = centro.municipio
    form.web.data = centro.web
    form.email.data = centro.email
    pdf = centro.protocolo
    form.coordenadas.data = centro.coordenadas
    return render_template('centros/validar_centro.html',
                        form=form,pdf=pdf,centro=centro)

@login_required
def devolver_centro_api(id):
    """
    Listar centro en particular via Api
    """ 
    if not check_permiso(current_user, 'centro_index'):
        abort(401)
    
    centro = Centro.buscar(id)
    if centro is None:
     return jsonify({'message':'401 Not Found'}),401 
    return centro_schema.jsonify(centro), 200

@login_required
def devolver_centros_api():
    """
    Listar centros via Api
    """
    if not check_permiso(current_user, 'centro_index'):
        abort(401)
    centros = Centro.devolvertodos()
    resultado = centros_schema.dump(centros) # con el dump, agarro todos los centros, y uso la variable centros_schema porque me voy a traer varios
    if centros is None:
     return ' 500 Internal server Error', 500
    return jsonify(resultado), 200            # convierte el resultado de string a formato json    


def agregar_centro_api():
    """
    agregar centros via Api
    """
    form = CentroForm
    data = request.get_json
    