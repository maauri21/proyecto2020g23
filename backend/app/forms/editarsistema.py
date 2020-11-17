from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length

# DataRequired es un validador de flaskwtf
class EditarConfigForm(FlaskForm):
    """
    Formulario de Configuracion
    """

    titulo = StringField(
        "Titulo",
        validators=[DataRequired(), Length(max=20, message="Máximo 20 caracteres")],
    )
    descripcion = StringField(
        "Descripcion",
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
    cantPaginacion = IntegerField(
        "Cantidad Paginacion", validators=[DataRequired("Número incorrecto")]
    )
    mantenimiento = BooleanField("Mantenimiento")
    submit = SubmitField("Aceptar")
