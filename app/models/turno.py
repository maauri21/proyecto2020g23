from app.db import db
from sqlalchemy.orm import validates
from flask import json
import string
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

    def json(self):
     return {
            "centro_id": self.centro_id,
            "email_donante": self.email,
            "hora_inicio": str(self.hora),
            "fecha": str(self.dia),
          
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

        if len(email) > 40:
            raise AssertionError(
                {"campo": "email", "mensaje": "El email no puede tener mas de 40 caracteres"}
            )       

        return email

       
    @validates("hora")
    def validate_hora(self, key, hora):
                 
                       
        if not str(hora):
            raise AssertionError(
                {"campo": "hora", "mensaje": "La hora no puede estar vacio"}
            )

        if not ":" in str(hora):
            raise AssertionError(
                {"campo": "hora", "mensaje": "La hora debe estar en el formato hh:mm"}
            )     
        
        if len(hora) != 5:
            raise AssertionError(
                {"campo": "hora", "mensaje": "La hora debe tener 5 caracteres"}
            ) 

        lista = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00"]
        
        if hora not in lista:
            raise AssertionError(
                {"campo": "hora", "mensaje": "La hora debe estar en el formato hh:mm"}
            )
        return hora