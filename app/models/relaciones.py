from app import db

usuario_rol = db.Table('usuario_rol',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

rol_permiso = db.Table('rol_permiso',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permisos.id'), primary_key=True)
)