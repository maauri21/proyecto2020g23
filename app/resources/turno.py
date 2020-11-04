from flask import (
    flash,
    redirect,
    render_template,
    url_for,
    request,
    abort,
    jsonify,
    json,
    session,
)
from flask_login import login_required, current_user

from app.forms.turno import TurnoForm
from app.forms.buscarturno import BuscarTurnoForm
from app.db import db
from app.models.turno import Turno
from app.models.centro import Centro
from app.models.configuracion import Configuracion
from app.helpers.permisos import check_permiso
from sqlalchemy import distinct
from datetime import date, timedelta

from werkzeug.utils import secure_filename
import os
import requests
from flask import current_app as app

@login_required
def buscar_turno():
    """
    Listar turnos
    """

    if not check_permiso(current_user, "turno_index"):
        abort(401)

    config = Configuracion.buscar_config()
    form = BuscarTurnoForm(formdata=request.args)

    # Para que no se rompa cuando busco guardo el id en sesion
    if (request.args.get("id")) is not None:
        centro = Centro.buscar(int(request.args.get("id")))
        session['centro'] = centro.id

    # Me traigo una vez (distinct) los email de los turnos de este centro (session)
    query = db.session.query(Turno.email, Turno.centro_id)
    query = query.filter(Turno.centro_id == session['centro'])
    query = query.distinct(Turno.email).group_by(Turno.email)

    for item in query:
        items = [(item.email, item.email)]
        form.select.choices += items

    estado = form.data["select"]
    pag = int(request.args.get("num_pag", 1))


    if form.data["select"] != "Todos":
        turnos = (
            Turno.query.filter(Turno.email.contains(estado))
            .filter(Turno.centro_id.contains(session['centro'])).order_by(Turno.turno.asc())
            .paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
        )
    else:
        # Turnos de hoy y 2 días más, ordenados
        turnos = Turno.query.filter(Turno.turno.between(date.today(), date.today() + timedelta(days=3))).order_by(Turno.turno.asc())
        # Que sean de este centro
        turnos = turnos.filter(Turno.centro_id.contains(session['centro'])).paginate(
            per_page=config.cantPaginacion, page=pag, error_out=False
        )
    return render_template("turnos/turnos.html", form=form, turnos=turnos, id=session['centro'])

@login_required
def agregar_turno(id):
    """
    Agregar turno
    """
    agregar_turno = True

    if not check_permiso(current_user, "turno_new"):
        abort(401)

    form = TurnoForm()

    return render_template(
        "turnos/turno.html", agregar_turno=agregar_turno, form=form
    )