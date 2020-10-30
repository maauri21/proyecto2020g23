from flask import flash, redirect, render_template, url_for, request, abort
from flask_login import login_required, current_user

from app.forms.registro import RegistroForm
from app.forms.buscarusuario import BuscarUsuarioForm
from app.forms.editarusuario import EditarUsuarioForm
from app.db import db
from app.models.usuario import Usuario
from app.models.configuracion import Configuracion
from app.helpers.permisos import check_permiso


@login_required
def buscar_usuarios():
    """
    Listar usuarios
    """

    if not check_permiso(current_user, "user_index"):
        abort(401)

    # Saber cuantos mostrar por pag
    config = Configuracion.query.first()
    form = BuscarUsuarioForm(formdata=request.args)
    buscar = form.data["search"]
    # Para volver a la misma pag dsp de cualquier acción
    # Si no recibo, setea 1
    # request.args=La parte de la URL después del signo de interrogación
    pag = int(request.args.get("num_pag", 1))
    # Activos + string de busqueda. Error out para que no me tire error cuando pongo un num de pag que no existe
    if form.data["select"] == "Activo":
        usuarios = (
            Usuario.query.filter_by(activo=True)
            .filter(Usuario.usuario.contains(buscar))
            .paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
        )
    elif form.data["select"] == "Bloqueado":
        usuarios = (
            Usuario.query.filter_by(activo=False)
            .filter(Usuario.usuario.contains(buscar))
            .paginate(per_page=config.cantPaginacion, page=pag, error_out=False)
        )
    # Todos
    else:
        usuarios = Usuario.query.filter(Usuario.usuario.contains(buscar)).paginate(
            per_page=config.cantPaginacion, page=pag, error_out=False
        )
    return render_template("usuarios/usuarios.html", form=form, usuarios=usuarios)


@login_required
def agregar_usuario():
    """
    Agregar usuario
    """
    agregar_usuario = True

    if not check_permiso(current_user, "user_new"):
        abort(401)

    form = RegistroForm()
    if form.validate_on_submit():
        try:
            usuario = Usuario(
                email=form.email.data,
                usuario=form.usuario.data,
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                password=form.password.data,
            )
            Usuario.add(usuario)
            Usuario.commit()
            flash("Usuario agregado")
        # Levanto las excepciones del modelo por sino pasa alguna validacion
        except AssertionError as e:
            # recorro el diccionario y listo el error de validacion correspondiente
            for elementos in e.args:
                form[elementos["campo"]].errors.append(elementos["mensaje"])
            return render_template(
                "usuarios/usuario.html", agregar_usuario=agregar_usuario, form=form
            )
        # Redirección al listado dsp de agregar
        return redirect(url_for("buscar_usuario"))

    return render_template(
        "usuarios/usuario.html", agregar_usuario=agregar_usuario, form=form
    )


@login_required
def editar_usuario(id):
    """
    Editar usuario
    """

    if not check_permiso(current_user, "user_update"):
        abort(401)

    agregar_usuario = False
    usuario = Usuario.buscar(id)
    form = EditarUsuarioForm()
    if form.validate_on_submit():

        try:
            usuario.email = form.email.data
            usuario.usuario = form.usuario.data
            usuario.nombre = form.nombre.data
            usuario.apellido = form.apellido.data
            Usuario.commit()
            flash("Usuario modificado")
        except AssertionError as e:
            for elementos in e.args:
                form[elementos["campo"]].errors.append(elementos["mensaje"])
            return render_template(
                "usuarios/usuario.html", agregar_usuario=agregar_usuario, form=form
            )
        return redirect(url_for("buscar_usuario"))

    form.email.data = usuario.email
    form.usuario.data = usuario.usuario
    form.nombre.data = usuario.nombre
    form.apellido.data = usuario.apellido
    return render_template(
        "usuarios/usuario.html", agregar_usuario=agregar_usuario, form=form
    )


@login_required
def bloquear_usuario(id):
    """
    Bloquear usuario
    """

    if not check_permiso(current_user, "user_state"):
        abort(401)

    usuario = Usuario.buscar(id)
    for rol in usuario.roles:
        if rol.nombre == "administrador":
            flash("No se puede bloquear a un administrador")
            return redirect(url_for("buscar_usuario"))
    Usuario.desactivar(usuario)
    Usuario.commit()
    flash("Usuario bloqueado")
    # Redirección al listado dsp de bloquear
    return redirect(url_for("buscar_usuario"))


@login_required
def activar_usuario(id):
    """
    Activar usuario
    """

    if not check_permiso(current_user, "user_state"):
        abort(401)

    usuario = Usuario.buscar(id)
    Usuario.activar(usuario)
    Usuario.commit()
    flash("Usuario activado")
    # Redirección al listado dsp de activar
    return redirect(url_for("buscar_usuario"))
