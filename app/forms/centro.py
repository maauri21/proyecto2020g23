from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TimeField,
    FileField,
    ValidationError,
    SelectField,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, Regexp
from app.models.tipocentro import TipoCentro
from flask_wtf.file import FileAllowed

# DataRequired es un validador de flaskwtf
class CentroForm(FlaskForm):
    """
    Formulario de agregar centro
    """

    nombre = StringField(
        "Nombre",
        validators=[DataRequired(), Length(max=40, message="Máximo 40 caracteres")],
    )
    direccion = StringField(
        "Dirección",
        validators=[DataRequired(), Length(max=40, message="Máximo 40 caracteres")],
    )
    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Length(max=20, message="Máximo 20 caracteres"),
            Regexp("^[0-9\-]+$", message="Solo números y -"),
        ],
        description="Insertar formato estilo 221-4808080",
    )
    apertura = TimeField(
        "Hora de apertura",
        format="%H:%M",
        validators=[DataRequired(message="Hora incorrecta")],
        description="Insertar formato estilo 12:10",
    )
    cierre = TimeField(
        "Hora de cierre",
        validators=[DataRequired(message="Hora incorrecta")],
        description="Insertar formato estilo 12:10",
    )
    tipo = QuerySelectField(
        "Tipo", validators=[DataRequired()], query_factory=TipoCentro.mostrar
    )
    municipio = SelectField("Municipio", choices=[])
    web = StringField(
        "Web", validators=[Length(max=40, message="Máximo 40 caracteres")]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email incorrecto"),
            Length(max=40, message="Máximo 40 caracteres"),
        ],
    )
    protocolo = FileField("Protocolo", validators=[FileAllowed(["pdf"], "Solo .pdf")])
    coordenadas = StringField(
        "Coordenadas",
        validators=[DataRequired(), Length(max=40, message="Máximo 40 caracteres")],
    )
    submit = SubmitField("Aceptar")

    def validate_cierre(form, field):
        if field.data < form.apertura.data:
            raise ValidationError("La hora de cierre debe ser mayor a la de apartura")
