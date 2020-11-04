from app.db import db

class Turno(db.Model):
    """
    Crear una tabla turnos
    """

    __tablename__ = "turnos"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40))
    dia = db.Column(db.Date())
    hora = db.Column(db.Time())
    centro_id = db.Column(db.Integer, db.ForeignKey("centros.id"))

    def __repr__(self):
        return self.email

    def agregar(turno):
        """
        Agrego el turno en la DB
        """
        db.session.add(turno)

    def commit():
        """
        Comiteo a la  DB
        """
        return db.session.commit()