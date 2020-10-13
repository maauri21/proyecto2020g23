from app import db
from app.models.relaciones import rol_permiso

class Rol(db.Model):
    """
    Crear una tabla roles
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    permisos = db.relationship('Permiso', secondary=rol_permiso)

    def __repr__(self):
        return '<Rol: {}>'.format(self.nombre)