from app.db import db

class Turno(db.Model):
    """
    Crear una tabla turnos
    """

    __tablename__ = "turnos"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40))
    turno = db.Column(db.DateTime())
    centro_id = db.Column(db.Integer, db.ForeignKey("centros.id"))

    def __repr__(self):
        return self.email