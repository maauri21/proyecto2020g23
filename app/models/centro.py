from app.db import db
from sqlalchemy.orm import validates
import string 

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
    lat = db.Column(db.String(15))
    lng = db.Column(db.String(15))
    tipo_id = db.Column(db.Integer, db.ForeignKey("tipocentros.id"))
    turnos = db.relationship("Turno", backref="centro", lazy=True)

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
                {"campo": "email", "mensaje": "El email no puede tener mas de 40 caracteres"}
            ) 

        if (centroAEditar is not None):
            if (email != centroAEditar.email):
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
        letras = string.ascii_letters + string.whitespace

        if not nombre:
            raise AssertionError(
                {"campo": "nombre", "mensaje": "El nombre no puede estar vacio"}
            )

        if len(nombre) > 40:
            raise AssertionError(
                {"campo": "nombre", "mensaje": "El nombre no puede tener mas de 40 caracteres"}
            )

        if (centroAEditar is not None):
            if (nombre != centroAEditar.nombre):
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
        expresion = (string.ascii_letters + string.whitespace + string.digits + ("#") + ("°") + (","))
        
        if not direccion:
            raise AssertionError(
                {"campo": "direccion", "mensaje": "La direccion no puede estar vacio"}
            )

        if len(direccion) > 40:
            raise AssertionError(
                {"campo": "direccion", "mensaje": "La direccion no puede tener mas de 40 caracteres"}
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
        expresion = (string.digits + (":"))
        
        if not str(apertura):
            raise AssertionError(
                {"campo": "apertura", "mensaje": "El horario de apertura no puede estar vacio"}
            )

        if not ":" in str(apertura):
            raise AssertionError(
                {"campo": "apertura", "mensaje": "El horario debe estar en el formato hh:mm"}
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
       expresion = (string.digits + (":"))
       
       if not str(cierre):
           raise AssertionError(
               {"campo": "cierre", "mensaje": "El horario de cierre no puede estar vacio"}
           )

       if not ":" in str(cierre):
            raise AssertionError(
                {"campo": "cierre", "mensaje": "El horario debe estar en el formato hh:mm"}
            ) 

        
       for elemento in str(cierre):
           if elemento not in expresion:              # transformo a string sino no puedo iterar sobre la hora, porque datetime no es un tipo iterable
               raise AssertionError(
                   {
                       "campo": "cierre",
                       "mensaje": "El horario de cierre solo puede contener numeros y : ",
                   }
               )
       return cierre   

    @validates("web")
    def validate_web(self, key, web):
       expresion = (string.printable)
       
              
       if not "." in web:
            raise AssertionError(
                {"campo": "web", "mensaje": "Ingrese una pagina web valida"}
            )    
        
       for elemento in web:
           if elemento not in expresion:              
               raise AssertionError(
                   {
                       "campo": "web",
                       "mensaje": "La pagina web puede contener solo numeros,letras y sinos de puntuacion ",
                   }
               )

               
       return web   

    @validates("telefono")
    def validate_telefono(self, key, telefono):
        expresion = (string.digits + ("-") )
        
        if not telefono:
            raise AssertionError(
                {"campo": "telefono", "mensaje": "El telefono no puede estar vacio"}
            )

        if len(telefono) > 40:
            raise AssertionError(
                {"campo": "telefono", "mensaje": "El telefono no puede tener mas de 40 caracteres"}
            )

        if len(telefono) < 8:
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
