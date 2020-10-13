from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, Length
from app.models.configuracion import Configuracion
from flask import session


# DataRequired es un validador de flaskwtf
class EditarConfigForm(FlaskForm):
    """
    Formulario de Configuracion
    """
    titulo = StringField('Titulo', validators=[DataRequired(), Length(max=20, message='Máximo 15 caracteres')])
    descripcion = StringField('Descripcion', validators=[DataRequired(), Length(max=40, message='Máximo 15 caracteres')])
    email = StringField('Email', validators=[DataRequired(), Email(message="Email incorrecto"), Length(max=40, message='Máximo 11 caracteres')])
    cantPaginacion = StringField('Cantidad Paginacion', validators=[DataRequired(), Length(max=3, message='Máximo 20 caracteres')])
    mantenimiento = BooleanField('Mantenimiento')
    submit = SubmitField('Aceptar')


