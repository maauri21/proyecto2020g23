from app import db

class Permiso(db.Model):
    """
    Crear una tabla permisos
    """
    __tablename__ = 'permisos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))

    def __repr__(self):
        return '<Permiso: {}>'.format(self.nombre)