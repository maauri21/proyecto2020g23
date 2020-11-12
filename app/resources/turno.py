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
        session["centro"] = centro.id

    # Me traigo una vez (distinct) los email de los turnos de este centro (session)
    email_distintos = Turno.email_distintos()

    for item in email_distintos:
        items = [(item.email, item.email)]
        form.select.choices += items

    email = form.data["select"]
    pag = int(request.args.get("num_pag", 1))

    if form.data["select"] != "Todos":
        turnos = Turno.buscar_con_email(email, session["centro"]).paginate(
            per_page=config.cantPaginacion, page=pag, error_out=False
        )
    else:
        # Turnos de hoy y 2 días más, ordenados
        turnos = Turno.hoy_y_2dias()
        # Que sean de este centro
        turnos = turnos.filter(Turno.centro_id.contains(session["centro"])).paginate(
            per_page=config.cantPaginacion, page=pag, error_out=False
        )
    return render_template(
        "turnos/turnos.html", form=form, turnos=turnos, id=session["centro"]
    )


@login_required
def agregar_turno(id):
    """
    Agregar turno
    """
    agregar_turno = True

    if not check_permiso(current_user, "turno_new"):
        abort(401)

    form = TurnoForm()
    form.centro_id.data = id
    turnos = Turno.turnos_ocupados(id, form.dia.data)

    if form.validate_on_submit():

        try:
            for item in turnos:
                if item.hora.strftime("%H:%M") == (form.hora.data):
                    flash("Turno ocupado")
                    return redirect(url_for("buscar_turno"))

            turno = Turno(
                email=form.email.data,
                dia=form.dia.data,
                hora=form.hora.data,
            )
            centro = Centro.buscar(id)
            centro.turnos.append(turno)
            Turno.agregar(turno)
            Turno.commit()
            flash("Turno agregado")

        except AssertionError as e:
            # recorro el diccionario y listo el error de validacion correspondiente
            for elementos in e.args:
                form[elementos["campo"]].errors.append(elementos["mensaje"])
            return render_template(
                "turnos/turno.html", agregar_turno=agregar_turno, form=form
            )
        return redirect(url_for("buscar_turno"))

    return render_template("turnos/turno.html", agregar_turno=agregar_turno, form=form)


@login_required
def editar_turno(id):
    """
    Editar turno
    """

    if not check_permiso(current_user, "turno_update"):
        abort(401)

    agregar_turno = False
    turno = Turno.buscar(id)

    form = TurnoForm()
    form.centro_id.data = turno.centro_id

    form.hora.choices += [(turno.hora.strftime("%H:%M"), turno.hora.strftime("%H:%M"))]

    if form.validate_on_submit():
        try:
            turno.email = form.email.data
            turno.dia = form.dia.data
            turno.hora = form.hora.data
            Turno.commit()
            flash("Turno modificado")
        except AssertionError as e:
            for elementos in e.args:
                form[elementos["campo"]].errors.append(elementos["mensaje"])
            return render_template(
                "turnos/turno.html", agregar_turno=agregar_turno, form=form, turno=turno
            )
        return redirect(url_for("buscar_turno"))

    form.email.data = turno.email
    form.dia.data = turno.dia
    return render_template(
        "turnos/turno.html", agregar_turno=agregar_turno, form=form, turno=turno
    )


@login_required
def borrar_turno(id):
    """
    Borrar turno
    """

    if not check_permiso(current_user, "turno_destroy"):
        abort(401)

    turno = Turno.buscar(id)

    Turno.eliminar(turno)
    Turno.commit()
    flash("Turno borrado")

    # Redirección al listado de turnos dsp de borrar
    return redirect(url_for("buscar_turno"))


def devolver_turnos_api(id):
    """
    Devolver turnos en api
    """
    # Si no puse fecha, le asigno la de hoy
    fecha = request.args.get("fecha", date.today().strftime("%Y-%m-%d"))

    centro = Centro.buscar(id)
    if centro is None or centro.estado != "Aceptado":
        return jsonify({"Error": "El centro no existe o no fue aceptado"}), 404

    try:
        valid_date = datetime.strptime(fecha, "%Y-%m-%d").date()
        if not (date(2020, 1, 1) <= valid_date <= date(2120, 1, 1)):
            raise ValueError()
    except ValueError:
        return jsonify({"Error": "Fecha inválida"})

    turnos_ocupados = Turno.turnos_ocupados(id, fecha)

    lista = []
    horario = datetime.strptime("08:30", "%H:%M")
    while horario < datetime.strptime("16:00", "%H:%M"):
        horario = horario + timedelta(minutes=30)
        lista.append(horario.strftime("%H:%M"))

    for item in turnos_ocupados:
        lista.remove(item.hora.strftime("%H:%M"))
    array = []
    for item in lista:
        horafin = datetime.strptime(item, "%H:%M") + timedelta(
            minutes=30
        )  # Lo convierto a time y le sumo 30
        diccionario = {
            "centro_id": id,
            "fecha": fecha,
            "hora_inicio": item,
            "horafin": horafin.strftime("%H:%M"),
        }
        array.append(diccionario)

    return jsonify({"turnos": array})


def registrar_turno_api(id):
    """
    Registrar turno en api
    """
    json = request.get_json(force=True)
    turnos = Turno.turnos_ocupados(id, json["fecha"])
    for item in turnos:
        if item.hora.strftime("%H:%M") == json["hora_inicio"]:
            return jsonify({"Error": "Turno ocupado"})
    try:
        turno = Turno(
            centro_id=id,
            email=json["email_donante"],
            hora=json["hora_inicio"],
            dia=json["fecha"],
        )

        centro = Centro.buscar(id)
        centro.turnos.append(turno)
        Turno.agregar(turno)
        Turno.commit()
    except AssertionError as e:
        for elementos in e.args:
            return jsonify({"Error": elementos["mensaje"]}), 400
    return jsonify({"atributos": turno.json()}), 201
