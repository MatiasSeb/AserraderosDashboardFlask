from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os
from config.database import db_url_users, db_url_data
from dotenv import load_dotenv
from flask_login import LoginManager


#inits
load_dotenv()
app = Flask(__name__)
rest_api = Api(app)


#configs
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url_users
db = SQLAlchemy(app)

#login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "basic"

#RUTAS
from controllers.usersController import usersapi
app.register_blueprint(usersapi)
