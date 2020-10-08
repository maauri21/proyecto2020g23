from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Usuario


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Agregar usuario a la BD a través del registro
    """
    # creo un modelo de empleado
    form = RegistrationForm()
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
        return redirect(url_for('auth.login'))

    # Cargar registro
    return render_template('auth/register.html', form=form, title='Registro')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login del usuario
    """
    form = LoginForm()
    if form.validate_on_submit():

        # Verifica que el empleado esté en BD
        # y su password coincida
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario is not None and usuario.verify_password(
                form.password.data):
            # Está y coincide: logea
            login_user(usuario)

            # Redirecciono al home
            return redirect(url_for('home.index'))

        # Si los datos no coinciden
        else:
            flash('Email o contraseña incorrecto')

    # Cargar login
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
# Debo estar logueado para poder hacer logout
@login_required
def logout():
    """
    Logout del usuario
    """
    logout_user()
    flash('Sesión cerrada correctamente')

    # Redirecciono a la página de login
    return redirect(url_for('auth.login'))