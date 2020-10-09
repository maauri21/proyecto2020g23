from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

#UserMixin es una clase de flasklogin que implementa métodos default
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), index=True, unique=True)
    usuario = db.Column(db.String(15), index=True, unique=True)
    nombre = db.Column(db.String(15))
    apellido = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    activo = db.Column(db.Boolean, default=True)

    # Prevenir que la contraseña sea accesible
    @property
    def password(self):
        raise AttributeError('Contraseña no es un atributo legible')

    # Hashear contraseña
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verificar que la pass coincide con la hasheada
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Usuario: {}>'.format(self.usuario)

# Usado por flask login 
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Configuracion(db.Model):
    __tablename__ = 'configuraciones'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(20))
    descripcion = db.Column(db.String(40))
    email = db.Column(db.String(20))
    cantPaginacion = db.Column(db.Integer)
    estadoSitio = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Configuracion: {}>'.format(self.titulo)