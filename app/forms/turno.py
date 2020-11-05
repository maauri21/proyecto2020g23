from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import DateField

class TurnoForm(FlaskForm):
    """
    Formulario de turnos
    """

    centro_id = HiddenField("centro_id")

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email incorrecto"),
            Length(max=40, message="Máximo 40 caracteres"),
        ],
    )

    dia = DateField('Dia')

    hora = SelectField("Hora", choices=[], validate_choice=False)

    submit = SubmitField("Aceptar")
