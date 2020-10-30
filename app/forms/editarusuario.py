from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp
from app.models.usuario import Usuario

# DataRequired es un validador de flaskwtf
class EditarUsuarioForm(FlaskForm):
    """
    Formulario de editar usuario
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
    submit = SubmitField("Aceptar")