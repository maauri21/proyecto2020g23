from app.db import db


class TipoCentro(db.Model):
    """
    Crear una tabla con los tipos de centro
    """

    __tablename__ = "tipocentros"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    centros = db.relationship("Centro", backref="tipo", lazy=True)

    def __repr__(self):
        return self.nombre

    def mostrar():
        return TipoCentro.query.all()

    def buscar_nombre(nombre):
        """
        Busco si el nombre está en la DB
        """
        return TipoCentro.query.filter_by(nombre=nombre).first()

    def buscar_id(id):
        """
        Busco si el id está en la DB
        """
        return TipoCentro.query.filter_by(id=id).first()
