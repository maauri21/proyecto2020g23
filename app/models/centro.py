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
    municipio = db.Column(db.String(30))
    web = db.Column(db.String(40))
    email = db.Column(db.String(40), index=True, unique=True)
    estado = db.Column(db.String(10))
    protocolo = db.Column(db.String(40))
    coordenadas = db.Column(db.String(40))
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipocentros.id'))

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

    def buscar(id):  
        """
        Busca la configuracion en la DB
        """
        return Centro.query.get(id)   

    def devolvertodos():  
        """
        Devuelve todos los centros de la db
        """
        return Centro.query.all()   

    def eliminar(centro): 
        """
        Elimina un centro en la DB
        """
        return db.session.delete(centro)

    def json(self):
        return {
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'hora_apertura': str(self.apertura),   #lo transformo a string sino jsonifi no puede serializarlo
            'hora_cierre': str(self.cierre),
            'tipo': self.tipo.nombre,
            'web': self.web,
            'email': self.email
        }

