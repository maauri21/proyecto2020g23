from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, HiddenField


class ValidarCentroForm(FlaskForm):
    """
    Formulario para validar centro
    """

    nombre = StringField("Nombre", render_kw={"readonly": True})
    direccion = StringField("Dirección", render_kw={"readonly": True})
    telefono = StringField("Teléfono", render_kw={"readonly": True})
    apertura = TimeField("Hora de apertura", render_kw={"readonly": True})
    cierre = TimeField("Hora de cierre", render_kw={"readonly": True})
    tipo = StringField("Tipo", render_kw={"readonly": True})
    municipio = StringField("Municipio", render_kw={"readonly": True})
    web = StringField("Web", render_kw={"readonly": True})
    email = StringField("Email", render_kw={"readonly": True})
    lat = HiddenField("lat")
    lng = HiddenField("lng")
    aceptar = SubmitField()
    rechazar = SubmitField()
