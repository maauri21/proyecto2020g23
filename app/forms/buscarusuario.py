from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class BuscarUsuarioForm(FlaskForm):
    search = StringField('Usuario', default='')
    select = SelectField('Estado:', choices=[('Todos', 'Todos'),('Activo', 'Activo'),('Bloqueado', 'Bloqueado')]) # (value, label)
    submit = SubmitField('Buscar')