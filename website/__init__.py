from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_mysqldb import MySQL
from os import path
import pymysql
import secrets

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ihdfsiuhdsufhusdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views

    app.register_blueprint(views,url_prefix='/')

    from .models import Students,Malzama,info

    create_db(app)

    return app


def create_db(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
