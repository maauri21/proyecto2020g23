from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, Regexp
from app.models.tipocentro import TipoCentro
from wtforms.fields.html5 import TimeField

# DataRequired es un validador de flaskwtf
class EditarCentroForm(FlaskForm):
    """
    Formulario de editar centro
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
            Length(min=7, message="Mínimo 7 caracteres"),
            Length(max=20, message="Máximo 20 caracteres"),
            Regexp("^[0-9\-]+$", message="Solo números y -"),
        ],
        description="Estilo 221-4808080",
    )
    apertura = TimeField(
        "Hora de apertura",
        format="%H:%M",
        validators=[DataRequired(message="Hora incorrecta")],
    )
    cierre = TimeField(
        "Hora de cierre", validators=[DataRequired(message="Hora incorrecta")]
    )
    tipo = QuerySelectField(
        "Tipo", validators=[DataRequired()], query_factory=TipoCentro.mostrar
    )
    municipio = SelectField("Municipio", choices=[])
    web = StringField(
        "Web",
        validators=[DataRequired(), Length(max=40, message="Máximo 40 caracteres")],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email incorrecto"),
            Length(max=40, message="Máximo 40 caracteres"),
        ],
    )
    lat = HiddenField("lat")
    lng = HiddenField("lng")
    submit = SubmitField("Aceptar")

    def validate_apertura(form, field):
        if field.data.strftime("%H:%M") > '09:00':
            raise ValidationError(
                "La hora de apertura debe ser menor o igual a las 09:00"
            )

    def validate_cierre(form, field):
        if field.data.strftime("%H:%M") < '16:00':
            raise ValidationError(
                "La hora de cierre debe ser mayor o igual a las 16:00"
            )
