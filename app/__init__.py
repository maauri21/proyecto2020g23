from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import app_config

# ORM
db = SQLAlchemy()
# Para manejar login, logout, sesiones
login_manager = LoginManager()

def create_app(config_name):
    """
    Cargar configuraciones
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(
            username=app.config["DB_USER"],
            password=app.config["DB_PASS"],
            host=app.config["DB_HOST"],
            database=app.config["DB_NAME"],
        )

    # No mostrar las modificaciones de los objetos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Para generar los formularios de forms.py y para mostrar los mensajes flash
    Bootstrap(app)
    # inicio app
    db.init_app(app)
    login_manager.init_app(app)
    # Si no está logueado muestra este mensaje y la vista para loguearse
    login_manager.login_message = "Debes estar logueado para acceder a esta página"
    login_manager.login_view = "auth.login"
    # para hacer migraciones
    migrate = Migrate(app, db)
    
    from app import models

    # registro cada blueprint
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app