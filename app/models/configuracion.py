from app import db

class Configuracion(db.Model):
    """
    Crear una tabla configuraciones
    """
    __tablename__ = 'configuraciones'

    titulo = db.Column(db.String(20), primary_key=True)
    descripcion = db.Column(db.String(40))
    email = db.Column(db.String(40))
    cantPaginacion = db.Column(db.Integer)
    mantenimiento = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Configuracion: {}>'.format(self.titulo)