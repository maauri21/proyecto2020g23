<<<<<<< HEAD
=======
# third-party imports
>>>>>>> 5a4286af0679cfdf1e5113bfd0b233c880b1826d
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # orm
from flask_login import LoginManager # registro, login, logout
from flask_migrate import Migrate # migraciones en la BD
from flask_bootstrap import Bootstrap # generar los formularios de forms.py y para mostrar los mensajes flash()
from config import app_config # imports locales

db = SQLAlchemy()
login_manager = LoginManager() # Para manejar login, logout, sesiones

# cargar configuraciones
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(
            username=app.config["DB_USER"],
            password=app.config["DB_PASS"],
            host=app.config["DB_HOST"],
            database=app.config["DB_NAME"],
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    Bootstrap(app)
<<<<<<< HEAD
    db.init_app(app)                # inicio app
=======
    db.init_app(app)
>>>>>>> 5a4286af0679cfdf1e5113bfd0b233c880b1826d
    login_manager.init_app(app)
    # Si no está logueado muestra este mensaje y la vista para loguearse
    login_manager.login_message = "Debes estar logueado para acceder a esta página"
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)  # Para hacer migraciones
    
    from app import models

    # registro cada blueprint
<<<<<<< HEAD
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
=======
    # Todas las vistas de admin serán accesibles desde /admin
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
>>>>>>> 5a4286af0679cfdf1e5113bfd0b233c880b1826d

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

<<<<<<< HEAD
    return app
=======
    return app
>>>>>>> 5a4286af0679cfdf1e5113bfd0b233c880b1826d
