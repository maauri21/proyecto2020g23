from app.db import db

class Centro(db.Model):
    """
    Crear una tabla centros
    """
    __tablename__ = 'centros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40))
    direccion = db.Column(db.String(40))
    telefono = db.Column(db.String(20))
    apertura = db.Column(db.Time())
    cierre = db.Column(db.Time())
    tipo = db.Column(db.String(30))
    municipio = db.Column(db.String(30))
    web = db.Column(db.String(40))
    email = db.Column(db.String(40))
    coordenadas = db.Column(db.String(40))
    estado = db.Column(db.String(10))

    def __repr__(self):
        return '<Centro: {}>'.format(self.nombre)