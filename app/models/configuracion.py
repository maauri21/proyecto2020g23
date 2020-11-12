from app.db import db


class Configuracion(db.Model):
    """
    Crear una tabla configuraciones
    """

    __tablename__ = "configuraciones"

    titulo = db.Column(db.String(20), primary_key=True)
    descripcion = db.Column(db.String(40))
    email = db.Column(db.String(40))
    cantPaginacion = db.Column(db.Integer)
    mantenimiento = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return "<Configuracion: {}>".format(self.titulo)

    def buscar_config():
        """
        Busca la configuracion en la DB
        """
        return Configuracion.query.first()

    def commit():
        """
        Comiteo a la DB
        """
        return db.session.commit()
