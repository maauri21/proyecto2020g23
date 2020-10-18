from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from app.db import db
from app.models.relaciones import usuario_rol

class Usuario(UserMixin, db.Model):
    """
    Crear una tabla usuarios, Usermixin es una clase de flasklogin que implementa métodos default
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), index=True, unique=True)
    usuario = db.Column(db.String(15), index=True, unique=True)
    nombre = db.Column(db.String(15))
    apellido = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    activo = db.Column(db.Boolean, default=True)
    roles = db.relationship('Rol', secondary=usuario_rol, lazy='subquery', backref=db.backref('usuarios', lazy=True))
    
    def tiene_permiso(user_id, permiso):
        """
        Busca si el usuario tiene el permiso y retorna True o False
        """
        # Agarro los roles del usuario y tengo los permisos de esos roles
        for rol in user_id.roles:
            for permi in rol.permisos:
                if (permi.nombre == permiso):
                    return True

    @property
    def password(self):
        """
        Prevenir que la contraseña sea accesible
        """
        raise AttributeError('Contraseña no es un atributo legible')

    @password.setter
    def password(self, password):
        """
        Hashear la contraseña
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verificar que la pass coincide con la hasheada
        """
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Usado por flask login para manejar al usuario logueado
        """
        return Usuario.query.get(int(user_id))

    def __repr__(self):
        return '<Usuario: {}>'.format(self.usuario)


    def add(usuario):
        """
        Agrego al usuario en la DB
        """
        db.session.add(usuario)
        
   
    def buscar_usuario(user_id):  
        """
        Busca al usuario en la DB
        """
        return Usuario.query.get(user_id)

    def commit():  
        """
        Comiteo a la  DB
        """
        
        return db.session.commit()

    
    def eliminar(usuario): 
        """
        Elimina un usuario en la DB
        """
        db.session.delete(usuario)
        return db.session.commit()     

    def desactivar(usuario): 
        """
        Cambia un usuario a desactivado
        """
        usuario.activo = False 

    def activar(usuario): 
        """
        Cambia un usuario a activado
        """
        usuario.activo = True    
