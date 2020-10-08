from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
<<<<<<< HEAD
from flask_login import current_user
=======

>>>>>>> 5a4286af0679cfdf1e5113bfd0b233c880b1826d
from ..models import Usuario


# DataRequired es un validador de flaskwtf
class RegistrationForm(FlaskForm):
    """
    Formulario de registro
    """
    email = StringField('Email', validators=[DataRequired(), Email(message="Email incorrecto")])
    usuario = StringField('Usuario', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(),EqualTo('confirm_password', message='La contraseña no coincide')])
    confirm_password = PasswordField('Confirmar contraseña')
<<<<<<< HEAD
    submit = SubmitField('Aceptar')
=======
    submit = SubmitField('Register')
>>>>>>> 5a4286af0679cfdf1e5113bfd0b233c880b1826d

    # Validar que el mail no esté usado
    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('Este email ya se encuentra en uso')

    # Validar que el usuario no esté usado
    def validate_usuario(self, field):
        if Usuario.query.filter_by(usuario=field.data).first():
            raise ValidationError('Este nombre de usuario ya se encuentra en uso')


class LoginForm(FlaskForm):
    """
    Formulario de login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Login')