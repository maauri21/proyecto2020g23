from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField
from wtforms.validators import DataRequired, Email, Length, Regexp
from app.models.centro import Centro

# DataRequired es un validador de flaskwtf
class CentroForm(FlaskForm):
    """
    Formulario de agregar/editar centro
    """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=40, message='Máximo 40 caracteres')])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=40, message='Máximo 40 caracteres')])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=20, message='Máximo 20 caracteres'), Regexp('^[0-9\-]+$', message='Solo números y -')])
    apertura = TimeField('Hora de apertura', validators=[DataRequired()])
    cierre = TimeField('Hora de cierre', validators=[DataRequired()])
    tipo = StringField('Tipo', validators=[DataRequired(), Length(max=30, message='Máximo 30 caracteres')])
    municipio = StringField('Municipio', validators=[DataRequired(), Length(max=30, message='Máximo 30 caracteres')])
    web = StringField('Web', validators=[DataRequired(), Length(max=40, message='Máximo 40 caracteres')])
    email = StringField('Email', validators=[DataRequired(), Email(message="Email incorrecto"), Length(max=40, message='Máximo 40 caracteres')])
    coordenadas = StringField('Coordenadas', validators=[DataRequired(), Length(max=40, message='Máximo 40 caracteres')])
    submit = SubmitField('Aceptar')