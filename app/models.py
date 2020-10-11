from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

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

    def __repr__(self):
        return '<Usuario: {}>'.format(self.usuario)

@login_manager.user_loader
def load_user(user_id):
    """
    Usado por flask login para manejar al usuario logueado
    """
    return Usuario.query.get(int(user_id))

class Configuracion(db.Model):
    """
    Crear una tabla configuraciones
    """
    __tablename__ = 'configuraciones'

    titulo = db.Column(db.String(20), primary_key=True)
    descripcion = db.Column(db.String(40))
    email = db.Column(db.String(40))
    cantPaginacion = db.Column(db.Integer)
    mantenimiento = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Configuracion: {}>'.format(self.titulo)