from app.db import db
from sqlalchemy.orm import validates
from flask import json
import string
from flask import session
from datetime import date, timedelta

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

    def buscar(id):
        """
        Busca un turno en la DB
        """
        return Turno.query.get(id)

    def eliminar(turno):
        """
        Elimina un turno en la DB
        """
        return db.session.delete(turno)   

    def email_distintos():
        """
        Email distintos de los que solicitaron turno en este centro
        """
        query = db.session.query(Turno.email, Turno.centro_id)
        query = query.filter(Turno.centro_id == session['centro'])
        query = query.distinct(Turno.email).group_by(Turno.email)
        return query

    def hoy_y_2dias():
        """
        Turnos de hoy y 2 días más, ordenados
        """
        return Turno.query.filter(Turno.dia.between(date.today(), date.today() + timedelta(days=2))).order_by(Turno.dia.asc(), Turno.hora.asc())

    def turnos_ocupados(id, fecha):
        """
        Devuelvo turnos ocupados
        """
        return Turno.query.filter_by(centro_id=id).filter_by(dia=fecha).all()

    def buscar_con_email(email, id):
        """
        Devuelvo los turnos para ese email
        """
        return Turno.query.filter(Turno.email.contains(email)).filter(Turno.centro_id.contains(id)).order_by(Turno.dia.asc(), Turno.hora.asc())

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

        lista = []
        horario = datetime.strptime('09:00', '%H:%M')
        while horario < datetime.strptime('16:00', '%H:%M'):
            horario = (horario + timedelta(minutes=30))
            lista.append(horario.strftime("%H:%M"))
        
        if hora not in lista:
            raise AssertionError(
                {"campo": "hora", "mensaje": "Hora incorrecta"}
            )
        return hora