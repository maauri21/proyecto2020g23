from flask import flash, redirect, render_template, url_for, session, request, abort
from flask_login import login_required, current_user

from app.forms.centro import CentroForm
from app.forms.buscarcentro import BuscarCentroForm
from app.db import db
from app.models.centro import Centro
from app.models.configuracion import Configuracion
from app.helpers.permisos import check_permiso

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
    pag = int(request.args.get('num_pag', 1))

    if form.data['select'] == 'Pendiente':
        centros = Centro.query.filter_by(Centro.estado.contains('pendiente')).filter(Centro.nombre.contains(buscar)).paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
    elif form.data['select'] == 'Aceptado':
        centros = Centro.query.filter_by(Centro.estado.contains('aceptado')).filter(Centro.nombre.contains(buscar)).paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
    elif form.data['select'] == 'Rechazado':
        centros = Centro.query.filter_by(Centro.estado.contains('rechazado')).filter(Centro.nombre.contains(buscar)).paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
    else:
        centros = Centro.query.filter(Centro.nombre.contains(buscar)).paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
    return render_template('centros/centros.html',
                            form=form,
                            centros=centros)
