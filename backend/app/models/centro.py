from app.db import db
from sqlalchemy.orm import validates
import string
import requests
from flask import json


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
    municipio = db.Column(db.String(3))
    web = db.Column(db.String(40))
    email = db.Column(db.String(40), index=True, unique=True)
    estado = db.Column(db.String(10))
    protocolo = db.Column(db.String(40))
    lat = db.Column(db.String(25))
    lng = db.Column(db.String(25))
    tipo_id = db.Column(db.Integer, db.ForeignKey("tipocentros.id"))
    turnos = db.relationship("Turno", backref="centro", lazy=True)

    def __repr__(self):
        return "<Centro: {}>".format(self.nombre)

    def agregar(centro):
        """
        Agrego el centro a la DB
        """
        db.session.add(centro)

    def crear(
        nombre,
        direccion,
        telefono,
        apertura,
        cierre,
        municipio,
        web,
        email,
        estado,
        protocolo,
        lat,
        lng,
    ):
        """
        Setea un centro
        """
        return Centro(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            apertura=apertura,
            cierre=cierre,
            municipio=municipio,
            web=web,
            email=email,
            estado=estado,
            protocolo=protocolo,
            lat=lat,
            lng=lng,
        )

    def commit():
        """
        Comiteo a la  DB
        """
        return db.session.commit()

    def buscar(id):
        """
        Busca un centro en la DB
        """
        return Centro.query.get(id)

    def devolvertodos():
        """
        Devuelve todos los centros de la db
        """
        return Centro.query.all()

    def eliminar(centro):
        """
        Baja lógica de un centro en la DB
        """
        centro.estado = 'Borrado'

    def cantidad():
        """
        Devuelve la cantidad de centros aceptados
        """
        return Centro.query.filter_by(estado="Aceptado").count()

    def buscar_estado(estado):
        """
        Busco el estado en la DB
        """
        return Centro.query.filter_by(estado=estado)

    def json(self):
        req = requests.get(
            "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135"
        )
        Jresponse = req.text
        data = json.loads(Jresponse)
        return {
            "nombre": self.nombre,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "hora_apertura": str(self.apertura),
            "hora_cierre": str(self.cierre),
            "municipio": data["data"]["Town"][str(self.municipio)]["name"],
            "tipo": self.tipo.nombre,
            "web": self.web,
            "email": self.email,
            "latitud": self.lat,
            "longitud": self.lng,
        }

    @validates("email")
    def validate_email(self, key, email):
        centroAEditar = Centro.query.get(self.id)
        if not email:
            raise AssertionError(
                {"campo": "email", "mensaje": "El email no puede estar vacio"}
            )
        if not "@" in email:
            raise AssertionError(
                {"campo": "email", "mensaje": "El email es incorrecto"}
            )

        if len(email) > 40:
            raise AssertionError(
                {
                    "campo": "email",
                    "mensaje": "El email no puede tener mas de 40 caracteres",
                }
            )

        if centroAEditar is not None:
            if email != centroAEditar.email:
                if Centro.query.filter(Centro.email == email).first():
                    raise AssertionError(
                        {
                            "campo": "email",
                            "mensaje": "Este email de centro ya se encuentra en uso",
                        }
                    )
        else:
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
        centroAEditar = Centro.query.get(self.id)
        letras = string.ascii_letters + string.whitespace + string.digits + ("ñ")

        if not nombre:
            raise AssertionError(
                {"campo": "nombre", "mensaje": "El nombre no puede estar vacio"}
            )

        if len(nombre) > 40:
            raise AssertionError(
                {
                    "campo": "nombre",
                    "mensaje": "El nombre no puede tener mas de 40 caracteres",
                }
            )

        if centroAEditar is not None:
            if nombre != centroAEditar.nombre:
                if Centro.query.filter(Centro.nombre == nombre).first():
                    raise AssertionError(
                        {
                            "campo": "nombre",
                            "mensaje": "Este nombre de centro ya se encuentra en uso",
                        }
                    )
        else:
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

    @validates("direccion")
    def validate_direccion(self, key, direccion):
        expresion = (
            string.ascii_letters
            + string.whitespace
            + string.digits
            + ("#")
            + ("°")
            + (",")
        )

        if not direccion:
            raise AssertionError(
                {"campo": "direccion", "mensaje": "La direccion no puede estar vacio"}
            )

        if len(direccion) > 40:
            raise AssertionError(
                {
                    "campo": "direccion",
                    "mensaje": "La direccion no puede tener mas de 40 caracteres",
                }
            )

        for elemento in direccion:
            if elemento not in expresion:
                raise AssertionError(
                    {
                        "campo": "direccion",
                        "mensaje": "La direccion solo puede contener letras, numeros , # Y ° ",
                    }
                )
        return direccion

    @validates("apertura")
    def validate_apertura(self, key, apertura):
        expresion = string.digits + (":")

        if not str(apertura):
            raise AssertionError(
                {
                    "campo": "apertura",
                    "mensaje": "El horario de apertura no puede estar vacio",
                }
            )

        if not ":" in str(apertura):
            raise AssertionError(
                {
                    "campo": "apertura",
                    "mensaje": "El horario debe estar en el formato hh:mm",
                }
            )

        if str(apertura) > '09:00:00':
            print (str(apertura))
            raise AssertionError(
                {
                    "campo": "apertura",
                    "mensaje": "La hora de apertura debe ser menor o igual a las 09:00",
                }
            )

        for elemento in str(apertura):
            if elemento not in expresion:
                raise AssertionError(
                    {
                        "campo": "apertura",
                        "mensaje": "El horario de apertura solo puede contener numeros y :, ingresar un formato del tipo hh:mm ",
                    }
                )
        return apertura

    @validates("cierre")
    def validate_cierre(self, key, cierre):
        expresion = string.digits + (":")

        if not str(cierre):
            raise AssertionError(
                {
                    "campo": "cierre",
                    "mensaje": "El horario de cierre no puede estar vacio",
                }
            )

        if not ":" in str(cierre):
            raise AssertionError(
                {
                    "campo": "cierre",
                    "mensaje": "El horario debe estar en el formato hh:mm",
                }
            )

        if str(cierre) < '16:00':
            raise AssertionError(
                {
                    "campo": "cierre",
                    "mensaje": "La hora de cierre debe ser mayor o igual a las 16:00",
                }
            )

        for elemento in str(cierre):
            if (
                elemento not in expresion
            ):  # transformo a string sino no puedo iterar sobre la hora, porque datetime no es un tipo iterable
                raise AssertionError(
                    {
                        "campo": "cierre",
                        "mensaje": "El horario de cierre solo puede contener numeros y : ",
                    }
                )
        return cierre

    @validates("municipio")
    def validate_direccion(self, key, municipio):
        expresion = string.digits

        if not municipio:
            raise AssertionError(
                {"campo": "municipio", "mensaje": "El municipio es obligatorio"}
            )

        for elemento in municipio:
            if elemento not in expresion:
                raise AssertionError(
                    {
                        "campo": "municipio",
                        "mensaje": "El municipio solo puede tener números",
                    }
                )

        if int(municipio) < 1 or int(municipio) > 135:
            raise AssertionError(
                {
                    "campo": "municipio",
                    "mensaje": "El municipio debe estar entre 1 y 135",
                }
            )

        return municipio

    @validates("web")
    def validate_web(self, key, web):
        expresion = string.printable

        for elemento in web:
            if elemento not in expresion:
                raise AssertionError(
                    {
                        "campo": "web",
                        "mensaje": "La pagina web puede contener solo numeros,letras y signos de puntuacion ",
                    }
                )

        return web

    @validates("telefono")
    def validate_telefono(self, key, telefono):
        expresion = string.digits + ("-")

        if not telefono:
            raise AssertionError(
                {"campo": "telefono", "mensaje": "El telefono no puede estar vacio"}
            )

        if len(telefono) > 40:
            raise AssertionError(
                {
                    "campo": "telefono",
                    "mensaje": "El telefono no puede tener mas de 40 caracteres",
                }
            )

        if len(telefono) < 7:
            raise AssertionError(
                {"campo": "telefono", "mensaje": "Ingrese un numero de telefono valido"}
            )

        for elemento in telefono:
            if elemento not in expresion:
                raise AssertionError(
                    {
                        "campo": "telefono",
                        "mensaje": "El telefono solo puede contener numeros y el caracter - , ingrese formato 221-4259320 ",
                    }
                )
        return telefono

    @validates("lat")
    def validate_lat(self, key, lat):
        expresion = string.digits + ("-") + (".")

        if not lat:
            raise AssertionError(
                {"campo": "lat", "mensaje": "El campo latitud no puede estar vacio"}
            )

        if len(lat) > 25:
            raise AssertionError(
                {
                    "campo": "lat",
                    "mensaje": "La latitud no puede tener mas de 25 caracteres",
                }
            )

        for elemento in lat:
            if elemento not in expresion:
                raise AssertionError(
                    {
                        "campo": "lat",
                        "mensaje": "El campo latitud solo puede contener numeros ",
                    }
                )
        return lat

    @validates("lng")
    def validate_lng(self, key, lng):
        expresion = string.digits + ("-") + (".")

        if not lng:
            raise AssertionError(
                {"campo": "lng", "mensaje": "El campo longitud no puede estar vacio"}
            )

        if len(lng) > 25:
            raise AssertionError(
                {
                    "campo": "lng",
                    "mensaje": "La longitud no puede tener mas de 25 caracteres",
                }
            )

        for elemento in lng:
            if elemento not in expresion:
                raise AssertionError(
                    {
                        "campo": "lng",
                        "mensaje": "El campo longitud solo puede contener numeros ",
                    }
                )
        return lng
