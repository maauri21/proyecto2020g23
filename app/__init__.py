from os import environ
from flask import Flask, render_template, request, url_for, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from app.helpers import handler
from config import config
from app.db import connection
from app.db import db

# Para manejar login, logout, sesiones. LoginManager se utiliza para guardar la configuración utilizada para la sesión
login_manager = LoginManager()

def create_app(environment="development"):
    """
    Cargar configuraciones
    """
    # Levanta la aplicación Flask. __name__ sirve para obtener el nombre de importación donde se define la app y Flask lo usa para saber donde buscar los resources, templates, static, etc.
    app = Flask(__name__)
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(
            username=app.config["DB_USER"],
            password=app.config["DB_PASS"],
            host=app.config["DB_HOST"],
            database=app.config["DB_NAME"],
        )

    app.config["SESSION_TYPE"] = "filesystem"

    # No mostrar las modificaciones de los objetos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Para generar los formularios de forms.py y para mostrar los mensajes flash
    Bootstrap(app)
    # Flask-Session
    Session(app)
    # inicio app
    connection(app)
    login_manager.init_app(app)
    # Si no está logueado muestra este mensaje y la vista para loguearse
    login_manager.login_message = "Debes estar logueado para acceder a esta página"
    login_manager.login_view = "auth_login"
    # para hacer migraciones
    migrate = Migrate(app, db)

    # orden para las migraciones
    from app.models import configuracion, rol, usuario, permiso, relaciones, centro

    from app.models.configuracion import Configuracion
    from app.resources import configuracion
    from app.resources import auth
    from app.resources import usuario
    from app.resources import centro

    # Para ocultar en los .html dependiendo los permisos
    from app.helpers import permisos
    app.jinja_env.globals.update(tiene_permiso=permisos.check_permiso)

    @app.route('/')
    def index():
        """
        Pagina principal
        """
        return render_template('index.html')

    @app.context_processor
    def mostrar_config():
        """
        context_processor se ejecuta antes que se procese la plantilla
        """
        config = Configuracion.query.first()
        return dict(mostrar_config=config)

    @app.before_request
    def verificar_mantenimiento():
        config = Configuracion.query.first()
        modo_mantenimiento = config.mantenimiento
        esAdmin=False
        # Si soy admin puedo navegar por la pag mientras hay mantenimiento
        if current_user.is_authenticated:
            for rol in current_user.roles:
                if (rol.nombre == 'administrador'):
                    esAdmin=True
        # Si estoy en modo mantenimiento y puse una url distinta a /login
        if modo_mantenimiento and request.path != url_for('auth_login'):
            if not esAdmin:
                return render_template('mantenimiento.html')

    #Handlers
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(404, handler.not_found_error)

    # Login
    app.add_url_rule("/login/", "auth_login", auth.login, methods=['GET', 'POST'])
    app.add_url_rule("/logout/", "auth_logout", auth.logout)

    # Usuarios
    app.add_url_rule("/usuarios/", "buscar_usuario", usuario.buscar_usuarios, methods=['GET', 'POST'])
    app.add_url_rule("/usuarios/agregar/", "agregar_usuario", usuario.agregar_usuario, methods=['GET', 'POST'])
    app.add_url_rule("/usuarios/editar/<int:id>", "editar_usuario", usuario.editar_usuario, methods=['GET', 'POST'])
    app.add_url_rule("/usuarios/borrar/<int:id>", "borrar_usuario", usuario.borrar_usuario)
    app.add_url_rule("/usuarios/bloquear/<int:id>", "bloquear_usuario", usuario.bloquear_usuario)
    app.add_url_rule("/usuarios/activar/<int:id>", "activar_usuario", usuario.activar_usuario)
    app.add_url_rule("/panelconfig/", "panel_config", configuracion.editar_configuracion, methods=['GET', 'POST'])

    # Centros
    app.add_url_rule("/centros/", "buscar_centros", centro.buscar_centros, methods=['GET', 'POST'])

    return app