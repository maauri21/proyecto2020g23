from app.db import db
from app.models.relaciones import rol_permiso

class Rol(db.Model):
    """
    Crear una tabla roles
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    permisos = db.relationship('Permiso', secondary=rol_permiso, lazy='subquery', backref=db.backref('roles', lazy=True))

    def __repr__(self):
        return '<Rol: {}>'.format(self.nombre)