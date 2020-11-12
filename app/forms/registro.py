from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

# DataRequired es un validador de flaskwtf
class RegistroForm(FlaskForm):
    """
    Formulario de agregar usuario
    """

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email incorrecto"),
            Length(max=40, message="Máximo 40 caracteres"),
        ],
    )
    usuario = StringField(
        "Usuario",
        validators=[DataRequired(), Length(max=15, message="Máximo 15 caracteres")],
    )
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(max=15, message="Máximo 15 caracteres"),
            Regexp(
                "^[a-zA-Z]+$", message="Números y caracteres especiales no permitidos"
            ),
        ],
    )
    apellido = StringField(
        "Apellido",
        validators=[
            DataRequired(),
            Length(max=20, message="Máximo 20 caracteres"),
            Regexp(
                "^[a-zA-Z]+$", message="Números y caracteres especiales no permitidos"
            ),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="La contraseña no coincide"),
            Length(max=20, message="Máximo 20 caracteres"),
        ],
    )
    confirm_password = PasswordField("Confirmar contraseña")
    submit = SubmitField("Aceptar")
