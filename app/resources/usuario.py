from flask import flash, redirect, render_template, url_for, session
from flask_login import login_required

from app.forms.registro import RegistroForm
from app.forms.buscarusuario import BuscarUsuarioForm
from app.forms.editarusuario import EditarUsuarioForm
from app import db
from app.models.usuario import Usuario
from app.models.configuracion import Configuracion

def register():
    """
    Agregar usuario a la BD a través del registro
    """
    # creo un modelo de empleado
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(email=form.email.data,
                            usuario=form.usuario.data,
                            nombre=form.nombre.data,
                            apellido=form.apellido.data,
                            password=form.password.data)

        # Lo guardo en BD
        db.session.add(usuario)
        db.session.commit()
        flash('Registro completado, completa el formulario para iniciar sesión')

        # Redirecciono a la página de login
        return redirect(url_for('auth_login'))

    # Cargar registro
    return render_template('auth/register.html', form=form)

@login_required
def buscar_usuarios(num_pag):
    """
    Listar usuarios
    """
    # Saber cuantos mostrar por pag
    config = Configuracion.query.first()
    form = BuscarUsuarioForm()
    buscar = form.data['search']
    # Para volver a la misma pag dsp de cualquier acción
    session['pag_usuario'] = num_pag
    # Activos + string de busqueda. Error out para que no me tire error cuando pongo un num de pag que no existe
    if form.data['select'] == 'Activo':
        usuarios = Usuario.query.filter_by(activo=True).filter(Usuario.usuario.contains(buscar)).paginate(per_page=config.cantPaginacion, page=num_pag, error_out=False)
    elif form.data['select'] == 'Bloqueado':
        usuarios = Usuario.query.filter_by(activo=False).filter(Usuario.usuario.contains(buscar)).paginate(per_page=config.cantPaginacion, page=num_pag, error_out=False)
    # Todos
    else:
        usuarios = Usuario.query.filter(Usuario.usuario.contains(buscar)).paginate(per_page=config.cantPaginacion, page=num_pag, error_out=False)
    return render_template('usuarios/usuarios.html', form=form, usuarios=usuarios)

@login_required
def redireccion_usuarios():
    """
    Para que no tire error si entro a /usuarios
    """
    return redirect(url_for('usuario_buscar', num_pag=1))

@login_required
def agregar_usuario():
    """
    Agregar usuario
    """
    agregar_usuario = True

    form = RegistroForm()
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
        return redirect(url_for('usuario_buscar', num_pag=session['pag_usuario']))

    return render_template('usuarios/usuario.html',
                           agregar_usuario=agregar_usuario, form=form)

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
        return redirect(url_for('usuario_buscar', num_pag=session['pag_usuario']))

    session['idEditar'] = id
    form.email.data = usuario.email
    form.usuario.data = usuario.usuario
    form.nombre.data = usuario.nombre
    form.apellido.data = usuario.apellido
    return render_template('usuarios/usuario.html',
                           agregar_usuario=agregar_usuario, form=form)

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
    return redirect(url_for('usuario_buscar', num_pag=session['pag_usuario']))

@login_required
def bloquear_usuario(id):
    """
    Bloquear usuario
    """
    usuario = Usuario.query.get_or_404(id)
    usuario.activo = False
    db.session.commit()
    flash('Usuario bloqueado')
    # Redirección al listado dsp de bloquear
    return redirect(url_for('usuario_buscar', num_pag=session['pag_usuario']))

@login_required
def activar_usuario(id):
    """
    Activar usuario
    """
    usuario = Usuario.query.get_or_404(id)
    usuario.activo = True
    db.session.commit()
    flash('Usuario activado')
    # Redirección al listado dsp de activar
    return redirect(url_for('usuario_buscar', num_pag=session['pag_usuario']))