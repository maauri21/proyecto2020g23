from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from app.models.usuario import Usuario

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

    # Validar que el mail no esté usado
    def validate_email(self, field):
        if Usuario.buscar_email(field.data):
            raise ValidationError("Este email ya se encuentra en uso")

    # Validar que el usuario no esté usado
    def validate_usuario(self, field):
        if Usuario.query.filter_by(usuario=field.data).first():
            raise ValidationError("Este nombre de usuario ya se encuentra en uso")
