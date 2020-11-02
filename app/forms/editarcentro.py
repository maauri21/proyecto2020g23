from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, ValidationError, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, Regexp
from app.models.tipocentro import TipoCentro

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
            Length(max=20, message="Máximo 20 caracteres"),
            Regexp("^[0-9\-]+$", message="Solo números y -"),
        ],
        description="Estilo 221-4808080",
    )
    apertura = TimeField(
        "Hora de apertura",
        format="%H:%M",
        validators=[DataRequired(message="Hora incorrecta")],
        description="Estilo 12:10",
    )
    cierre = TimeField(
        "Hora de cierre",
        validators=[DataRequired(message="Hora incorrecta")],
        description="Estilo 12:10",
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
    coordenadas = StringField(
        "Coordenadas",
        validators=[DataRequired(), Length(max=40, message="Máximo 40 caracteres")],
    )
    submit = SubmitField("Aceptar")

    def validate_cierre(form, field):
       if field.data < form.apertura.data:
            raise ValidationError("La hora de cierre debe ser mayor a la de apartura")
