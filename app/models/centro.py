from app.db import db
from flask_marshmallow import Marshmallow

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

    def buscar_centro(id):  
        """
        Busca la configuracion en la DB
        """
        return Centro.query.get(id)   

    def devolvertodos():  
        """
        Devuelve todos los centros de la db
        """
        return Centro.query.all()       

ma = Marshmallow()

# creo el schema con el cual voy a devolver los campos cuando se acceda a la info via api
class CentroSchema(ma.Schema):
        class Meta:
            fields = ('id', 'nombre', 'direccion', 'telefono', 'apertura', 'cierre', 'tipo', 'municipio', 'web', 'email', 'coordenadas', 'estado')    


# creo 2 variables, una para devolver un centro y otra en caso de que quiera devolver varios    
centro_schema = CentroSchema()
centros_schema = CentroSchema(many=True)