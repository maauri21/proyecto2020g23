from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from datetime import date, timedelta


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

    dia = SelectField(
        "Dia:",
        choices=[
            (date.today().strftime("%d/%m/%Y"), date.today().strftime("%d/%m/%Y")),
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

    hora = SelectField(
        "Hora:",
        choices=[
            ('09:00', '09:00'),
            ('09:30', '09:30'),
            ('10:00', '10:00'),
            ('10:30', '10:30'),
            ('11:00', '11:00'),
            ('11:30', '11:30'),
            ('12:00', '12:00'),
            ('12:30', '12:30'),
            ('13:00', '13:00'),
            ('13:30', '13:30'),
            ('14:00', '14:00'),
            ('14:30', '14:30'),
            ('15:00', '15:00'),
            ('15:30', '15:30'),
            ('16:00', '16:00'),
        ],
    )

    submit = SubmitField("Aceptar")
