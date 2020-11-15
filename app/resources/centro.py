from flask import (
    flash,
    redirect,
    render_template,
    url_for,
    request,
    abort,
    jsonify,
    json,
)
from flask_login import login_required, current_user

from app.forms.centro import CentroForm
from app.forms.editarcentro import EditarCentroForm
from app.forms.validar_centro import ValidarCentroForm
from app.forms.buscarcentro import BuscarCentroForm
from app.db import db
from app.models.centro import Centro
from app.models.tipocentro import TipoCentro
from app.models.configuracion import Configuracion
from app.helpers.permisos import check_permiso

from werkzeug.utils import secure_filename
import os
import requests
from flask import current_app as app
import math


@login_required
def buscar_centros():
    """
    Listar centros
    """

    if not check_permiso(current_user, "centro_index"):
        abort(401)

    config = Configuracion.buscar_config()
    form = BuscarCentroForm(formdata=request.args)
    buscar = form.data["search"]
    estado = form.data["select"]
    pag = int(request.args.get("num_pag", 1))

    if form.data["select"] != "Todos":
        centros = (
            Centro.query.filter(Centro.estado.contains(estado))
            .filter(Centro.nombre.contains(buscar))
            .paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
        )
    else:
        centros = Centro.query.filter(Centro.nombre.contains(buscar)).paginate(
            per_page=config.cantPaginacion, page=pag, error_out=False
        )
    return render_template("centros/centros.html", form=form, centros=centros)

@login_required
def agregar_centro():
    """
    Agregar centro
    """
    agregar_centro = True

    if not check_permiso(current_user, "centro_new"):
        abort(401)

    # Hago un request para agarrar los municipios de la API
    req = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135"
    )
    # Guardo todo en data para dsp recorrer el índice
    Jresponse = req.text
    data = json.loads(Jresponse)

    form = CentroForm()
    i = str(1)
    for item in data["data"]["Town"]:
        items = [(data["data"]["Town"][i]["id"], data["data"]["Town"][i]["name"])]
        form.municipio.choices += items
        i = int(i)
        i += 1
        i = str(i)

    if form.validate_on_submit():
        tipo = form.tipo.data
        file = form.protocolo.data
        filename = secure_filename(file.filename)
        nombreArchivo = None
        if file:
            # Por si suben 2 archivos con el mismo nombre, lo renombro poniendole el nombre del centro 1ro
            nombreArchivo = form.nombre.data + "_" + filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo))

        try:
            centro = Centro.crear(
                form.nombre.data,
                form.direccion.data,
                form.telefono.data,
                form.apertura.data,
                form.cierre.data,
                form.municipio.data,
                form.web.data,
                form.email.data,
                "Aceptado",
                nombreArchivo,
                form.lat.data,
                form.lng.data,
            )
            tipo.centros.append(centro)
            Centro.agregar(centro)
            Centro.commit()
            flash("Centro agregado")
        # Levanto las excepciones del modelo por sino pasa alguna validacion
        except AssertionError as e:
            # recorro el diccionario y listo el error de validacion correspondiente
            for elementos in e.args:
                form[elementos["campo"]].errors.append(elementos["mensaje"])
            return render_template(
                "centros/centro.html", agregar_centro=agregar_centro, form=form
            )
        # Redirección al listado dsp de agregar
        return redirect(url_for("buscar_centros"))

    return render_template(
        "centros/centro.html", agregar_centro=agregar_centro, form=form
    )


@login_required
def editar_centro(id):
    """
    Editar centro
    """

    if not check_permiso(current_user, "centro_update"):
        abort(401)

    agregar_centro = False
    centro = Centro.buscar(id)

    # Agarrar los municipios de la API
    req = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135"
    )
    Jresponse = req.text
    data = json.loads(Jresponse)

    form = EditarCentroForm()
    i = str(1)
    for item in data["data"]["Town"]:
        items = [(data["data"]["Town"][i]["id"], data["data"]["Town"][i]["name"])]
        form.municipio.choices += items
        i = int(i)
        i += 1
        i = str(i)

    if form.validate_on_submit():
        try:
            centro.nombre = form.nombre.data
            centro.direccion = form.direccion.data
            centro.telefono = form.telefono.data
            centro.apertura = form.apertura.data
            centro.cierre = form.cierre.data
            centro.tipo = form.tipo.data
            centro.municipio = form.municipio.data
            centro.web = form.web.data
            centro.email = form.email.data
            centro.lat = form.lat.data
            centro.lng = form.lng.data
            Centro.commit()
            flash("Centro modificado")
        except AssertionError as e:
            for elementos in e.args:
                form[elementos["campo"]].errors.append(elementos["mensaje"])
            return render_template(
                "centros/centro.html",
                agregar_centro=agregar_centro,
                form=form,
                centro=centro,
            )
        # Redirección al listado dsp de agregar
        return redirect(url_for("buscar_centros"))

    form.nombre.data = centro.nombre
    form.direccion.data = centro.direccion
    form.telefono.data = centro.telefono
    form.apertura.data = centro.apertura
    form.cierre.data = centro.cierre
    form.tipo.data = centro.tipo
    form.municipio.data = centro.municipio
    form.web.data = centro.web
    form.email.data = centro.email
    form.lat.data = centro.lat
    form.lng.data = centro.lng
    return render_template(
        "centros/centro.html", agregar_centro=agregar_centro, form=form, centro=centro
    )


@login_required
def borrar_centro(id):
    """
    Borrar centro
    """

    if not check_permiso(current_user, "centro_destroy"):
        abort(401)

    centro = Centro.buscar(id)

    # Borrar el archivo si subió pdf
    if centro.protocolo is not None:
        os.unlink(os.path.join(app.config["UPLOAD_FOLDER"], centro.protocolo))

    Centro.eliminar(centro)
    Centro.commit()
    flash("Centro borrado")

    # Redirección al listado dsp de borrar
    return redirect(url_for("buscar_centros"))


@login_required
def validar_centro(id):
    """
    Validar centro
    """

    if not check_permiso(current_user, "centro_validate"):
        abort(401)

    centro = Centro.buscar(id)
    form = ValidarCentroForm()
    if form.validate_on_submit():
        if form.aceptar.data:
            centro.estado = "Aceptado"
        elif form.rechazar.data:
            centro.estado = "Rechazado"
        Centro.commit()
        flash("Centro validado")
        return redirect(url_for("buscar_centros"))

    form.nombre.data = centro.nombre
    form.direccion.data = centro.direccion
    form.telefono.data = centro.telefono
    form.apertura.data = centro.apertura
    form.cierre.data = centro.cierre
    form.tipo.data = centro.tipo.nombre
    form.lat.data = centro.lat
    form.lng.data = centro.lng

    # Agarrar el nombre teniendo el id (centro.municipio)
    req = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135"
    )
    Jresponse = req.text
    data = json.loads(Jresponse)
    form.municipio.data = data["data"]["Town"][str(centro.municipio)]["name"]

    form.web.data = centro.web
    form.email.data = centro.email
    pdf = centro.protocolo
    return render_template(
        "centros/validar_centro.html", form=form, pdf=pdf, centro=centro
    )


def devolver_centros_api():
    """
    Listar centros via Api
    """

    page = int(request.args.get("num_pag", 1))
    config = Configuracion.buscar_config()
    centros = Centro.buscar_estado("Aceptado").paginate(
        per_page=config.cantPaginacion, page=page, error_out=False
    )

    cant_centrosAceptados = Centro.cantidad()
    total = cant_centrosAceptados / config.cantPaginacion

    resultado = [centro.json() for centro in centros.items]

    return jsonify(
        {"centros": resultado}, {"total": math.ceil(total)}, {"pagina": page}
    )


def devolver_centro_api(id):
    """
    Listar un centro es especifico via Api
    """

    centro = Centro.buscar(id)
    if centro is None or centro.estado != "Aceptado":
        return jsonify({"Error": "El centro no existe o no fue aceptado"}), 404
    return jsonify({"atributos": centro.json()}), 200


def registrar_centro_api():
    """
    Crear centro via Api
    """

    json = request.get_json(force=True)

    if json.get("nombre") is None:
        abort(400)

    try:
        tipo = TipoCentro.buscar_nombre(json["tipo"])
        if tipo is None:
            return jsonify({"Error": "Este tipo de centro no existe"})

        centro = Centro.crear(
            json["nombre"],
            json["direccion"],
            json["telefono"],
            json["hora_apertura"],
            json["hora_cierre"],
            json["municipio"],
            json["web"],
            json["email"],
            "Pendiente",
            None,
            json["latitud"],
            json["longitud"],
        )

        tipo.centros.append(centro)
        Centro.agregar(centro)
        Centro.commit()
    except AssertionError as e:
        for elementos in e.args:
            return jsonify({"Error": elementos["mensaje"]}), 400
    return jsonify({"atributos": centro.json()}), 201
