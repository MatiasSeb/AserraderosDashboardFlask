from flask import Blueprint, render_template, make_response, Response, request, redirect, url_for, flash
from flask_login import login_required
from forms.forms import CreateDBConnForm, EditDBConnForm, DeleteForm
from controllers.databaseController import *

databaseRoutes = Blueprint('databaseRoutes', __name__)


@databaseRoutes.route("/admin/config_db")
@login_required
def admin_config_dbconn():
    createconnform = CreateDBConnForm()
    editconnform = EditDBConnForm()
    deleteconnform = DeleteForm()
    
    conns = getConnections()
    return render_template("admin_config_dbconn.html", createconnform=createconnform, editconnform=editconnform, deleteconnform=deleteconnform, conns=conns)

@databaseRoutes.route("/admin/config_db", methods=['POST'])
@login_required
def create_conn():
    createconnform = CreateDBConnForm()
    if createconnform.validate_on_submit():
        connection_name = createconnform.connection_name.data
        conn_username = createconnform.conn_username.data
        conn_password = createconnform.conn_password.data
        conn_ip = createconnform.conn_ip.data
        conn_port = createconnform.conn_port.data
        conn_dbname = createconnform.conn_dbname.data
        
        if createConnection(connection_name, conn_username, conn_password, conn_ip, conn_port, conn_dbname):
            flash("Conexión creada")
            return redirect(url_for('databaseRoutes.admin_config_dbconn'))
        else:
            print (createconnform.errors)
            flash('Hubo un error en el formulario')
            return redirect(url_for('databaseRoutes.admin_config_dbconn'))
    return 'Form not submitted'

@databaseRoutes.route("/admin/config_db/<int:_id>", methods=['GET', 'POST'])
@login_required
def update_conn(_id):
    from models.databasesModels import Databases
    databaseToFind = Databases.query.get_or_404(_id)
    
    editconnform = EditDBConnForm(obj=databaseToFind)
    
    if request.method == 'POST' and editconnform.validate_on_submit():
        connection_name = editconnform.connection_name.data
        conn_username = editconnform.conn_username.data
        conn_password = editconnform.conn_password.data
        conn_ip = editconnform.conn_ip.data
        conn_port = editconnform.conn_port.data
        conn_dbname = editconnform.conn_dbname.data
        
        if updateConnection(_id, connection_name, conn_username, conn_password, conn_ip, conn_port, conn_dbname):
            print('conexión modificada')
            return redirect(url_for('databaseRoutes.admin_config_dbconn'))
        else:
            print (editconnform.errors)

@databaseRoutes.route("/admin/config_db/delete_<int:_id>", methods=['GET', 'POST'])
@login_required
def delete_conn(_id):
    deleteconnform = DeleteForm()
    if deleteconnform.validate_on_submit():
        if deleteConnection(_id):
            response = make_response('Success: Conexion eliminada')
            response.headers['Content-Type'] = 'text/plain'
            return response
        else:
            flash('Hubo un error al eliminar la conexion')
            response = make_response('Error: Hubo un error al eliminar la conexion')
            response.headers['Content-Type'] = 'text/plain'
            return response

@databaseRoutes.route("/admin/config_data")
@login_required
def admin_config_data():
    return render_template("admin_config_data.html")