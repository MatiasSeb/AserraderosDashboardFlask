from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
from flask_login import login_required
from forms.forms import CreateDBConnForm, EditDBConnForm, DeleteForm, DatabaseForm
from controllers.databaseController import *
from models.databasesModels import Databases
from models.settingModels import GlobalSettings
import asyncio

databaseRoutes = Blueprint('databaseRoutes', __name__)

@databaseRoutes.route("/admin/config_db")
@login_required
def admin_config_dbconn():
    createconnform = CreateDBConnForm()
    editconnform = EditDBConnForm()
    deleteconnform = DeleteForm()
    
    conns = getConnections()
    
    return render_template("/admin/config_dbconn.html", createconnform=createconnform, editconnform=editconnform, deleteconnform=deleteconnform, conns=conns)

@databaseRoutes.route("/admin/config_db", methods=['POST'])
@login_required
async def create_conn():
    createconnform = CreateDBConnForm()
    if createconnform.validate_on_submit():
        connection_name = createconnform.connection_name.data
        conn_username = createconnform.conn_username.data
        conn_ip = createconnform.conn_ip.data
        conn_port = createconnform.conn_port.data
        conn_dbname = createconnform.conn_dbname.data
        if createConnection(connection_name, conn_username, conn_ip, conn_port, conn_dbname):
            message = "Conexión creada"
            response = make_response(jsonify({'status': 'success', 'message': message}), 200)
            print(response.get_json)
            return redirect(url_for('databaseRoutes.admin_config_dbconn'))
        else:
            message = (f"Error: {createconnform.errors}")
            response = make_response(jsonify({'status': 'error', 'message': message}), 400)
            print(response.get_json)
            return redirect(url_for('databaseRoutes.admin_config_dbconn'))

@databaseRoutes.route("/admin/config_db/<int:_id>", methods=['GET', 'POST'])
@login_required
async def update_conn(_id):
    databaseToFind = Databases.query.get_or_404(_id)
    
    editconnform = EditDBConnForm(obj=databaseToFind)
    
    if request.method == 'POST' and editconnform.validate_on_submit():
        connection_name = editconnform.connection_name.data
        conn_username = editconnform.conn_username.data
        conn_ip = editconnform.conn_ip.data
        conn_port = editconnform.conn_port.data
        conn_dbname = editconnform.conn_dbname.data
        
        if updateConnection(_id, connection_name, conn_username, conn_ip, conn_port, conn_dbname):
            message = (f'Conexión modificada:{_id, ":", connection_name}')
            response = make_response(jsonify({'status': 'success', 'message': message}), 200)
            print(response.get_json())
            return redirect(url_for('databaseRoutes.admin_config_dbconn'))
        else:
            message = (f'Hubo algún error al actualizar el usuario:{editconnform.errors}')
            response = make_response(jsonify({'status': 'success', 'message': message}), 400)
            print(response.get_json())
            return redirect(url_for('databaseRoutes.admin_config_dbconn'))

@databaseRoutes.route("/admin/config_db/delete_<int:_id>", methods=['GET', 'POST'])
@login_required
async def delete_conn(_id):
    deleteconnform = DeleteForm()
    if deleteconnform.validate_on_submit():
        if deleteConnection(_id):
            message = ("Conexión eliminada correctamente", _id)
            response = make_response(jsonify({'status': 'success', 'message': message}), 200)
            print(response.get_json())
            return redirect(url_for('databaseRoutes.admin_config_dbconn'))
    else:
        message = (f"Hubo un error al eliminar:{deleteconnform.errors}")
        response = make_response(jsonify({'status': 'error', 'message': message}))
        print(response.get_json())
        return redirect(url_for('databaseRoutes.admin_config_dbconn'))

#No se si aquí deba ir la api que toma la base de datos elegida
@databaseRoutes.route("/admin/config_data", methods=['GET'])
@login_required
async def admin_config_data():
    conns = getConnections()
    is_streaming = await GlobalSettings.is_streaming_data()
    if is_streaming == 'True':
        chosen_table = await GlobalSettings.get_chosen_table()
        
        return render_template("admin/config_data.html", is_streaming=is_streaming, chosen_table=chosen_table)
    if is_streaming == 'False':
        dbform = DatabaseForm()
        databaseChoices = [(conn._id, f"{conn._id}. Usuario: {conn.conn_username}" " - " f"Nombre de la BD: {conn.conn_dbname}, Dirección IP: {conn.conn_ip}:{conn.conn_port} ") for conn in conns]
        dbform.selected_conn.choices = databaseChoices
        return render_template("admin/config_data.html", is_streaming=is_streaming, conns=conns, dbform=dbform)

@databaseRoutes.route("/admin/config_data", methods=['POST'])
@login_required
async def get_tables_with_conn():
    dbform = DatabaseForm()
    conn_id = dbform.selected_conn.data
    
    if dbform.validate_on_submit():
        selected_bd = Databases.getConnById(conn_id)
        db_pwd = dbform.db_pwd.data
        conn_result = uriDatabaseBuilder(selected_bd, db_pwd)
        if conn_result is not None:
            tables = getSelectedDatabase(conn_result) 
            if tables:
                message = 'Credenciales verificadas, y conexión establecida con el servidor. Obteniendo información'
                response = make_response(jsonify({'status': 'success', 'message': message}), 201)
                print(response.get_json())
                return render_template(admin_config_data, tables) 
            else:
                message = 'No hay tablas en la base de datos, verifica la conexión o tu base de datos a conectar.'
                response = make_response(jsonify({'status': 'success-2', 'message': message}), 202)
                print(response.get_json())
                return response
    else:
        message = (f"Contraseña incorrecta u otro error procedente del formulario: {dbform.errors}")
        response = make_response(jsonify({'status': 'error', 'message': message}), 402)
        print(response.get_json())
        return response

@databaseRoutes.route("/admin/config_data", methods=['POST'])
@login_required
async def stream_selected():
    pass