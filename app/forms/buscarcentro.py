from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class BuscarCentroForm(FlaskForm):
    search = StringField('Nombre', default='')
    select = SelectField('Estado:', choices=[('Todos', 'Todos'),('Pendiente', 'Pendiente'),('Aceptado', 'Aceptado'),('Rechazado', 'Rechazado')]) # (value, label)
    submit = SubmitField('Buscar')