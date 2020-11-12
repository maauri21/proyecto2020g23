from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app.forms.login import LoginForm
from app.models.usuario import Usuario


def login():
    """
    Login del usuario
    """
    form = LoginForm()
    if form.validate_on_submit():

        usuario = Usuario.buscar_email(form.email.data)
        # Datos correctos pero bloqueado
        if (
            usuario is not None
            and usuario.verify_password(form.password.data)
            and usuario.activo == False
        ):
            flash("Usuario bloqueado")
        elif usuario is not None and usuario.verify_password(form.password.data):
            # Está y coincide: logea
            login_user(usuario)
            # Redirecciono al home
            return redirect(url_for("index"))
        # Si los datos no coinciden
        else:
            flash("Email o contraseña incorrecto")

    # Cargar login
    return render_template("auth/login.html", form=form)


# Debo estar logueado para poder hacer logout
@login_required
def logout():
    """
    Logout del usuario
    """
    logout_user()
    flash("Sesión cerrada correctamente")

    # Redirecciono a la página de login
    return redirect(url_for("auth_login"))
