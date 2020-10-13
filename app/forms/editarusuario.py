from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp
from app.models.usuario import Usuario
from flask import session


# DataRequired es un validador de flaskwtf
class EditarUsuarioForm(FlaskForm):
    """
    Formulario de registro
    """
    email = StringField('Email', validators=[DataRequired(), Email(message="Email incorrecto"), Length(max=40, message='Máximo 40 caracteres')])
    usuario = StringField('Usuario', validators=[DataRequired(), Length(max=15, message='Máximo 15 caracteres')])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=15, message='Máximo 15 caracteres'), Regexp('^[a-zA-Z]+$', message='Números y caracteres especiales no permitidos')])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=20, message='Máximo 20 caracteres'), Regexp('^[a-zA-Z]+$', message='Números y caracteres especiales no permitidos')])
    submit = SubmitField('Aceptar')

    # Validar que el mail no esté usado
    def validate_email(self, field):
        idSesion = session['idEditar']
        usuarioAEditar = Usuario.query.filter_by(id=idSesion).first()       # Agarro el usuario que estoy editando
        if field.data != usuarioAEditar.email:                              # Si el mail es distinto al que estoy editando, valido (xq le cambié el mail)
            if Usuario.query.filter_by(email=field.data).first():           # Valido que no se repita con algun otro
                raise ValidationError('Este email ya se encuentra en uso')

    # Validar que el usuario no esté usado
    def validate_usuario(self, field):
        idSesion = session['idEditar']
        usuarioAEditar = Usuario.query.filter_by(id=idSesion).first()
        if field.data != usuarioAEditar.usuario:    
            if Usuario.query.filter_by(usuario=field.data).first():
                raise ValidationError('Este nombre de usuario ya se encuentra en uso')