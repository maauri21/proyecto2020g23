import pymysql

from flask import current_app
from flask import g
from flask import cli
from config import config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()





def connection(app):
    db.init_app(app)
    app.teardown_request(close)



def close(exception):
        
    db.session.remove()
    db.engine.dispose()