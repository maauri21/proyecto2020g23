from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Length
from datetime import date, timedelta


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

    dia = SelectField(
        "Dia:",
        choices=[
            (date.today(), date.today()),
            (
                (date.today() + timedelta(days=1)).strftime("%d/%m/%Y"),
                (date.today() + timedelta(days=1)).strftime("%d/%m/%Y"),
            ),
            (
                (date.today() + timedelta(days=2)).strftime("%d/%m/%Y"),
                (date.today() + timedelta(days=2)).strftime("%d/%m/%Y"),
            ),
                        (
                (date.today() + timedelta(days=3)).strftime("%d/%m/%Y"),
                (date.today() + timedelta(days=3)).strftime("%d/%m/%Y"),
            ),
                        (
                (date.today() + timedelta(days=4)).strftime("%d/%m/%Y"),
                (date.today() + timedelta(days=4)).strftime("%d/%m/%Y"),
            ),
                        (
                (date.today() + timedelta(days=5)).strftime("%d/%m/%Y"),
                (date.today() + timedelta(days=5)).strftime("%d/%m/%Y"),
            ),
                        (
                (date.today() + timedelta(days=6)).strftime("%d/%m/%Y"),
                (date.today() + timedelta(days=6)).strftime("%d/%m/%Y"),
            ),
                        (
                (date.today() + timedelta(days=7)).strftime("%d/%m/%Y"),
                (date.today() + timedelta(days=7)).strftime("%d/%m/%Y"),
            ),
        ],
    )

    hora = SelectField("Hora", choices=[])

    submit = SubmitField("Aceptar")
