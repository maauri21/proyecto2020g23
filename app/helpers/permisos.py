from app.models.usuario import Usuario

def check_permiso(user_id, permiso):
    return Usuario.tiene_permiso(user_id, permiso)