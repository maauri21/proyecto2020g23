from flask import flash, redirect, render_template, url_for, session
from flask_login import login_required

from . import admin
from ..auth.forms import RegistrationForm
from .forms import EditarUsuarioForm, BuscadorUsuario
from .. import db
from ..models import Usuario

@admin.route('/usuarios/', methods=['GET', 'POST'])
@login_required
def buscar_usuarios():
    """
    Listar usuarios
    """
    # Al principio muestro todos
    usuarios=Usuario.query.all()
    form = BuscadorUsuario()
    buscar = form.data['search']
    # Activos + string de busqueda
    if form.data['select'] == 'Activo':
        usuarios = Usuario.query.filter_by(activo=True).filter(Usuario.usuario.contains(buscar))
    elif form.data['select'] == 'Bloqueado':
        usuarios = Usuario.query.filter_by(activo=False).filter(Usuario.usuario.contains(buscar))
    else:
        usuarios = Usuario.query.filter(Usuario.usuario.contains(buscar))   
    return render_template('admin/usuarios/usuarios.html', form=form, usuarios=usuarios)

@admin.route('/usuarios/agregarusuario/', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    """
    Agregar usuario
    """
    agregar_usuario = True

    form = RegistrationForm()
    if form.validate_on_submit():
        usuario = Usuario(email=form.email.data,
                            usuario=form.usuario.data,
                            nombre=form.nombre.data,
                            apellido=form.apellido.data,
                            password=form.password.data)

        db.session.add(usuario)
        db.session.commit()
        flash('Usuario agregado')

        # Redirección al listado dsp de agregar
        return redirect(url_for('admin.buscar_usuarios'))

    return render_template('admin/usuarios/usuario.html',
                           agregar_usuario=agregar_usuario, form=form)


@admin.route('/usuarios/edititarusuario/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    """
    Editar usuario
    """
    agregar_usuario = False

    usuario = Usuario.query.get_or_404(id)
    form = EditarUsuarioForm()
    if form.validate_on_submit():
        usuario.email = form.email.data
        usuario.usuario = form.usuario.data
        usuario.nombre = form.nombre.data
        usuario.apellido = form.apellido.data
        db.session.commit()
        flash('Usuario modificado')

        # Redirección al listado dsp de editar
        return redirect(url_for('admin.buscar_usuarios'))

    session['idEditar'] = id
    form.email.data = usuario.email
    form.usuario.data = usuario.usuario
    form.nombre.data = usuario.nombre
    form.apellido.data = usuario.apellido
    return render_template('admin/usuarios/usuario.html',
                           agregar_usuario=agregar_usuario, form=form,
                           usuario=usuario)


@admin.route('/usuarios/borrarusuario/<int:id>', methods=['GET', 'POST'])
@login_required
def borrar_usuario(id):
    """
    Borrar usuario
    """
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario borrado')

    # Redirección al listado dsp de borrar
    return redirect(url_for('admin.buscar_usuarios'))

@admin.route('/paneladmin/')
@login_required
def panel_admin():
    """
    Panel de configuración del admin
    """
    return render_template('admin/paneladmin.html')