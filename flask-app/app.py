from flask import Flask
from flask_restful import Api
import os
from config.database import create_engine, create_Database, db_url, db_usersdbname, load_dotenv
from config.extensions import db, login_manager
from flask_bcrypt import Bcrypt

#inits
load_dotenv()
rest_api = Api()
bcrypt = Bcrypt()

#app factory
def create_app():
    #init app and rest api
    app = Flask(__name__)
    rest_api.init_app(app)
    
    #configs
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    #database setups
    engine = create_engine(db_url + db_usersdbname)
    create_Database(engine, db_usersdbname)
    app.config['SQLALCHEMY_DATABASE_URI']=db_url + db_usersdbname

    #init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    bcrypt.init_app(app)

    #RUTAS
    with app.app_context():
        from routes.userRoute import userRoutes
        from routes.databaseRoute import databaseRoutes
        app.register_blueprint(userRoutes)
        app.register_blueprint(databaseRoutes)
    
    return app

