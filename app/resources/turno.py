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
from datetime import date, timedelta, datetime

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
            .filter(Turno.centro_id.contains(session['centro'])).order_by(Turno.dia.asc(), Turno.hora.asc())
            .paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
        )
    else:
        # Turnos de hoy y 2 días más, ordenados
        turnos = Turno.query.filter(Turno.dia.between(date.today(), date.today() + timedelta(days=2))).order_by(Turno.dia.asc(), Turno.hora.asc())
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

    turnos_ocupados = Turno.query.filter_by(centro_id=id).all()
    lista = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00"]
    
    for item in turnos_ocupados:
        lista.remove(item.hora.strftime("%H:%M"))

    for item in lista:
        form.hora.choices += [(item, item)]

    if form.validate_on_submit():
        turno = Turno(
            email=form.email.data,
            dia=datetime.strptime(form.dia.data, '%d/%m/%Y'),
            hora=form.hora.data,
        )
        centro = Centro.buscar(id)
        centro.turnos.append(turno)
        Turno.agregar(turno)
        Turno.commit()
        flash("Turno agregado")
        return redirect(url_for("buscar_turno"))

    return render_template(
        "turnos/turno.html", agregar_turno=agregar_turno, form=form
    )


def devolver_turnos_api(id):
    """
    Devolver turnos en api
    """

    fecha = request.args.get("fecha")

    turnos_ocupados = Turno.query.filter_by(centro_id=id).filter_by(dia=fecha).all()

    # hacerlo con while
    lista = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00"]
    
    for item in turnos_ocupados:
        lista.remove(item.hora.strftime("%H:%M"))
    # usar un map en vez de array con for
    array = []
    for item in lista:
        diccionario = {'centro_id':id, 'fecha':fecha, 'hora_inicio':item, 'horafin':'09:30'}
        array.append(diccionario)

    return jsonify({"turnos": array})


