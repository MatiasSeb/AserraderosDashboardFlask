from flask import Flask
import os
from config.database import create_engine, create_Database, db_url, db_usersdbname, load_dotenv
from config.extensions import db, login_manager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

#inits
load_dotenv()
bcrypt = Bcrypt()
socketio = SocketIO()
migrate = Migrate()

#app factory
def create_app():
    #init app and rest api
    app = Flask(__name__)
        
    #configs
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    #database setups
    engine = create_engine(db_url + db_usersdbname)
    create_Database(engine, db_usersdbname)
    app.config['SQLALCHEMY_DATABASE_URI']=db_url + db_usersdbname
    app.config['SQLALCHEMY_POOL_SIZE'] = 10  # Set the maximum number of connections in the pool
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600  # Set the maximum age of a connection in the pool (in seconds)
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30 
    
    #init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    #init migrate
    import models
    migrate.init_app(app, db)
    
    #login configurations
    login_manager.session_protection = "strong"
    login_manager.login_view = 'userRoutes.login'
    

    #RUTAS
    with app.app_context():
        from routes.userRoute import userRoutes
        from routes.databaseRoute import databaseRoutes
        app.register_blueprint(userRoutes)
        app.register_blueprint(databaseRoutes)
    
    return app

