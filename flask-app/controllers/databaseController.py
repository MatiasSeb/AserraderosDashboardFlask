from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import time, random

def getConnections():
    from models.databasesModels import Databases
    
    dbconns = Databases.query.all()
    if not dbconns:
        return 'No connections found'
    else:
        return dbconns

def createConnection(connection_name, conn_username, conn_password, conn_ip, conn_port, conn_dbname):
    from models.databasesModels import Databases, db
    
    if connection_name and conn_username and conn_ip and conn_port and conn_dbname:
        if conn_password:
            hashed_dbpwd = Databases.generate_password(conn_password)
        newDb = Databases(connection_name, conn_username, hashed_dbpwd, conn_ip, conn_port, conn_dbname)
        db.session.add(newDb)
        db.session.commit()
        return newDb
    else:
        error_message = "Some required fields are missing. Please fill in all the required fields."
        return error_message

def updateConnection(_id, connection_name, conn_username, conn_password, conn_ip, conn_port, conn_dbname):
    from models.databasesModels import Databases, db
    dbToUpdate = Databases.query.get(_id)
    if not dbToUpdate:
        return 'db not found'
    else:
        if connection_name and conn_username and conn_ip and conn_port and conn_dbname:
            if conn_password:
                dbToUpdate.password = Databases.generate_password(conn_password)
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
    from models.databasesModels import Databases, db
    
    dbToDelete = Databases.query.get_or_404(_id)
    if dbToDelete:
        db.session.delete(dbToDelete)
        db.session.commit()
    else:
        return 'no funciona'