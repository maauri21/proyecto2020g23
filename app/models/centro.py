from app.db import db

class Centro(db.Model):
    """
    Crear una tabla centros
    """
    __tablename__ = 'centros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), index=True, unique=True)
    direccion = db.Column(db.String(40))
    telefono = db.Column(db.String(20))
    apertura = db.Column(db.Time())
    cierre = db.Column(db.Time())
    tipo = db.Column(db.String(30))
    municipio = db.Column(db.String(30))
    web = db.Column(db.String(40))
    email = db.Column(db.String(40), index=True, unique=True)
    estado = db.Column(db.String(10))
    protocolo = db.Column(db.String(40))
    coordenadas = db.Column(db.String(40))

    def __repr__(self):
        return '<Centro: {}>'.format(self.nombre)

    def agregar(centro):
        """
        Agrego el centro a la DB
        """
        db.session.add(centro)

    def commit():  
        """
        Comiteo a la  DB
        """
        return db.session.commit()