from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import current_user
from ..models import Usuario
from flask import session


# DataRequired es un validador de flaskwtf
class EditarUsuarioForm(FlaskForm):
    """
    Formulario de registro
    """
    email = StringField('Email', validators=[DataRequired(), Email(message="Email incorrecto")])
    usuario = StringField('Usuario', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    submit = SubmitField('Aceptar')

    # Validar que el mail no esté usado
    def validate_email(self, field):
        idSesion = session['idEditar']
        usuarioAEditar = Usuario.query.filter_by(id=idSesion).first()
        if field.data != usuarioAEditar.email:    
            if Usuario.query.filter_by(email=field.data).first():
                raise ValidationError('Este email ya se encuentra en uso')

    # Validar que el usuario no esté usado
    def validate_usuario(self, field):
        idSesion = session['idEditar']
        usuarioAEditar = Usuario.query.filter_by(id=idSesion).first()
        if field.data != usuarioAEditar.usuario:    
            if Usuario.query.filter_by(usuario=field.data).first():
                raise ValidationError('Este nombre de usuario ya se encuentra en uso')