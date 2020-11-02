from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateTimeField,
)
from wtforms.validators import DataRequired, Email, Length

class TurnoForm(FlaskForm):
    """
    Formulario de turnos
    """

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email incorrecto"),
            Length(max=40, message="Máximo 40 caracteres"),
        ],
    )

    turno = DateTimeField(
        "Turno",
#        format="%H:%M",
        validators=[DataRequired()]
    )

    submit = SubmitField("Aceptar")
