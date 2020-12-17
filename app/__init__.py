from os import environ
from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
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
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql+pymysql://{username}:{password}@{host}/{database}".format(
        username=app.config["DB_USER"],
        password=app.config["DB_PASS"],
        host=app.config["DB_HOST"],
        database=app.config["DB_NAME"],
    )

    app.config["SESSION_TYPE"] = "filesystem"

    # No mostrar las modificaciones de los objetos
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Donde meto los pdf
    app.config["UPLOAD_FOLDER"] = "app/static/uploads"

    # Para que la API se duvuelva en el orden que quiero
    app.config["JSON_SORT_KEYS"] = False

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
    from app.models import (
        configuracion,
        rol,
        usuario,
        permiso,
        relaciones,
        tipocentro,
        centro,
        turno,
    )

    from app.models.configuracion import Configuracion
    from app.resources import configuracion
    from app.resources import auth
    from app.resources import usuario
    from app.resources import centro
    from app.resources import turno
    from app.resources import estadistica

    # Para ocultar en los .html dependiendo los permisos
    from app.helpers import permisos

    app.jinja_env.globals.update(tiene_permiso=permisos.check_permiso)

    @app.route("/")
    def index():
        """
        Pagina principal
        """
        return render_template("index.html")

    @app.context_processor
    def mostrar_config():
        """
        context_processor se ejecuta antes que se procese la plantilla
        """
        config = Configuracion.buscar_config()
        return dict(mostrar_config=config)

    @app.before_request
    def verificar_mantenimiento():
        config = Configuracion.buscar_config()
        modo_mantenimiento = config.mantenimiento
        esAdmin = False
        # Si soy admin puedo navegar por la pag mientras hay mantenimiento
        if current_user.is_authenticated:
            for rol in current_user.roles:
                if rol.nombre == "administrador":
                    esAdmin = True
        # Si estoy en modo mantenimiento y puse una url distinta a /login
        if modo_mantenimiento and request.path != url_for("auth_login"):
            if not esAdmin:
                return render_template("mantenimiento.html")

    #Handlers
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(500, handler.internal_server_error_api)
    app.register_error_handler(400, handler.bad_request_error_api)


    # Login
    app.add_url_rule("/login/", "auth_login", auth.login, methods=['GET', 'POST'])
    app.add_url_rule("/logout/", "auth_logout", auth.logout)

    # Usuarios
    app.add_url_rule("/usuarios/", "buscar_usuario", usuario.buscar_usuarios, methods=['GET', 'POST'])
    app.add_url_rule("/usuarios/agregar/", "agregar_usuario", usuario.agregar_usuario, methods=['GET', 'POST'])
    app.add_url_rule("/usuarios/editar/<int:id>", "editar_usuario", usuario.editar_usuario, methods=['GET', 'POST'])
    app.add_url_rule("/usuarios/bloquear/<int:id>", "bloquear_usuario", usuario.bloquear_usuario)
    app.add_url_rule("/usuarios/activar/<int:id>", "activar_usuario", usuario.activar_usuario)
    app.add_url_rule("/panelconfig/", "panel_config", configuracion.editar_configuracion, methods=['GET', 'POST'])

    # Centros
    app.add_url_rule("/centros/", "buscar_centros", centro.buscar_centros, methods=['GET', 'POST'])
    app.add_url_rule("/centros/agregar/", "agregar_centro", centro.agregar_centro, methods=['GET', 'POST'])
    app.add_url_rule("/centros/editar/<int:id>", "editar_centro", centro.editar_centro, methods=['GET', 'POST'])
    app.add_url_rule("/centros/borrar/<int:id>", "borrar_centro", centro.borrar_centro)
    app.add_url_rule("/centros/validar/<int:id>", "validar_centro", centro.validar_centro, methods=['GET', 'POST'])
    app.add_url_rule("/api/v1/centros", "devolver_centros_api", centro.devolver_centros_api, methods=['GET'])
    app.add_url_rule("/api/v1/centros/<int:id>", "devolver_centro_api", centro.devolver_centro_api, methods=['GET'])
    app.add_url_rule("/api/v1/centros", "registrar_centros_api", centro.registrar_centro_api, methods=['POST'])

    # Turnos
    app.add_url_rule("/centros/turnos/", "buscar_turno", turno.buscar_turno, methods=['GET', 'POST'])
    app.add_url_rule("/centros/<int:id>/turnos/agregar/", "agregar_turno", turno.agregar_turno, methods=['GET', 'POST']) 
    app.add_url_rule("/centros/turnos/borrar/<int:id>", "borrar_turno", turno.borrar_turno)
    app.add_url_rule("/centros/turnos/editar/<int:id>", "editar_turno", turno.editar_turno, methods=['GET', 'POST'])
    app.add_url_rule("/api/v1/centros/<int:id>/turnos_disponibles/", "devolver_turnos_api", turno.devolver_turnos_api, methods=['GET'])
    app.add_url_rule("/api/v1/centros/<int:id>/reserva", "registrar_turno_api", turno.registrar_turno_api, methods=['POST'])

    # Estadísticas

    app.add_url_rule("/api/v1/estadisticas/tipos_mas_utilizados", "tipos_mas_utilizados", estadistica.tipos_mas_utilizados, methods=['GET'])
    app.add_url_rule("/api/v1/estadisticas/municipios_mas_concurridos", "municipios_mas_concurridos", estadistica.municipios_mas_concurridos, methods=['GET'])

    return app