from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from app.models.turno import Turno

class BuscarTurnoForm(FlaskForm):

    select = SelectField("Email", choices=[("Todos", "Todos")],
        default="Todos")

    submit = SubmitField("Buscar")
