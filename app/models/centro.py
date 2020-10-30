from app.db import db
from sqlalchemy.orm import validates
from flask import jsonify


class Centro(db.Model):
    """
    Crear una tabla centros
    """

    __tablename__ = "centros"

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
    tipo_id = db.Column(db.Integer, db.ForeignKey("tipocentros.id"))

    def __repr__(self):
        return "<Centro: {}>".format(self.nombre)

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
            "nombre": self.nombre,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "hora_apertura": str(
                self.apertura
            ),  # lo transformo a string sino jsonifi no puede serializarlo
            "hora_cierre": str(self.cierre),
            "tipo": self.tipo.nombre,
            "web": self.web,
            "email": self.email,
        }

    @validates("email")
    def validate_email(self, key, email):

        if not email:
            raise AssertionError(
                {"campo": "email", "mensaje": "El email no puede estar vacio"}
            )
        if not "@" in email:
            raise AssertionError(
                {"campo": "email", "mensaje": "El email es incorrecto"}
            )
        if Centro.query.filter(Centro.email == email).first():
            raise AssertionError(
                {
                    "campo": "email",
                    "mensaje": "Este email de centro ya se encuentra en uso",
                }
            )
        return email

    @validates("nombre")
    def validate_nombre(self, key, nombre):

        letras = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "ñ",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "Ñ",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            " ",
        ]

        if not nombre:
            raise AssertionError(
                {"campo": "nombre", "mensaje": "El nombre no puede estar vacio"}
            )
        if Centro.query.filter(Centro.nombre == nombre).first():
            raise AssertionError(
                {
                    "campo": "nombre",
                    "mensaje": "Este nombre de centro ya se encuentra en uso",
                }
            )
        for elemento in nombre:
            if elemento not in letras:
                raise AssertionError(
                    {
                        "campo": "nombre",
                        "mensaje": "El nombre solo puede contener letras",
                    }
                )
        return nombre
