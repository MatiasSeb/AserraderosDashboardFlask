from models.databasesModels import Databases, db
from models.settingModels import GlobalSettings
from sqlalchemy import create_engine
from flask import jsonify, current_app
from app import socketio

#CRUD DATABASE
def getConnections(): 
    dbconns = Databases.query.all()
    if not dbconns:
        return []
    else:
        return dbconns

def createConnection(connection_name, conn_username, conn_ip, conn_port, conn_dbname):    
    if connection_name and conn_username and conn_ip and conn_port and conn_dbname:
        newDb = Databases(connection_name, conn_username, conn_ip, conn_port, conn_dbname)
        db.session.add(newDb)
        db.session.commit()
        return newDb
    else:
        error_message = "Some required fields are missing. Please fill in all the required fields."
        return error_message

def updateConnection(_id, connection_name, conn_username, conn_ip, conn_port, conn_dbname):
    dbToUpdate = Databases.query.get(_id)
    if not dbToUpdate:
        return 'db not found'
    else:
        if connection_name and conn_username and conn_ip and conn_port and conn_dbname:
            dbToUpdate.connection_name = connection_name
            dbToUpdate.conn_username = conn_username
            dbToUpdate.conn_ip = conn_ip
            dbToUpdate.conn_port = conn_port
            dbToUpdate.conn_dbname = conn_dbname
            db.session.commit()
            return dbToUpdate
        else:
            return ' no funciona'

def deleteConnection(_id):    
    try:
        dbToDelete = Databases.query.get_or_404(_id)
        if dbToDelete is None:
            raise Exception("Connection does not exist")
        db.session.delete(dbToDelete)
        db.session.commit()
    except Exception as e:
        return ("Hubo algun error en la eliminación:", e) and False
    return True



def uriDatabaseBuilder(selected_bd, db_pwd):
    db_host = selected_bd.conn_host
    db_port = selected_bd.conn_port
    db_name = selected_bd.conn_dbname
    db_user = selected_bd.conn_username
    db_password = db_pwd

    db_uri = f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    current_app.config['SQLALCHEMY_BINDS'][db_name] = db_uri
    engine = db.get_engine(bind=db_name)
    return engine

def getSelectedDatabase(engine):
    try:
        
        with engine.connect() as conn:
            with engine.connect() as conn:
                result = conn.execute("SHOW TABLES")
                tables = [row[0] for row in result]
            if tables:
                # Connection successful
                return tables
            else:
                # Connection failed
                return False
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return False

def streamSelectedTable(db_uri, table):
    try:
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            with engine.connect() as conn:
                result = conn.execute(f"SELECT * FROM {table}")
                data = [dict(row) for row in result]
            if data:
                GlobalSettings.query.filter_by(setting_name='is_streaming').update(setting_value='True')
                GlobalSettings.query.filter_by(setting_name='chosen_table').update(setting_value=f'{table}')
                db.session.commit()
                socketio.emit('update', data)
                return data
            else:
                return False
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return False

