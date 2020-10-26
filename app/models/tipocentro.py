from app.db import db
from app import ma
from marshmallow import fields
class TipoCentro(db.Model):
    """
    Crear una tabla con los tipos de centro
    """
    __tablename__ = 'tipocentros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    centros = db.relationship('Centro', backref='tipo', lazy=True)

    def __repr__(self):
        return self.nombre

    def mostrar():      
        return TipoCentro.query.all()

class TipoCentroSchema(ma.Schema):
    
    nombre = fields.String()
    
             

tipocentro_schema = TipoCentroSchema()