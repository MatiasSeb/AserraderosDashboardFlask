from flask import Blueprint, render_template, make_response, request, redirect, url_for, jsonify
from config.extensions import login_manager
from controllers.userController import *
from models.userModels import User
from models.settingModels import GlobalSettings
from flask_login import login_required, logout_user, current_user
from forms.forms import FirstRegistrationForm, LoginForm, CreateUserForm, EditUserForm, DeleteForm
import asyncio
from helpers.responses import create_error_response, create_success_response

userRoutes = Blueprint('userRoutes', __name__)

@login_manager.user_loader
def load_user(_id):
    return User.query.get(_id)

#RUTAS APLICACIÓN FLASK
#LOGIN USUARIOS
@userRoutes.route("/login", methods=['GET', 'POST'])
async def login():
    form = LoginForm(request.form)
    
    if request.method == 'GET':
        message = create_success_response("Bienvenido al acceso de usuarios", 200)
        return render_template('/login.html', form=form, message=message)
    
    elif request.method == 'POST':
        email = form.email.data
        password = form.pwd.data
    
        if form.validate_on_submit():
            login_result = loginUser(email, password)
    
            if login_result == 1:
                message = create_success_response("Admin conectado.", 200)
                return redirect(url_for('userRoutes.pasarela')), message
    
            elif login_result == 2:
                message = create_success_response("Usuario conectado.", 200)
                return redirect(url_for('platform')), message
    
            elif login_result == 3:
                message = create_error_response("Contraseña incorrecta", 400)
                return redirect(url_for('userRoutes.login')) 
    
            elif login_result == 4:
                message = create_error_response("Usuario no encontrado.", 400)
                return redirect(url_for('userRoutes.login')) 
    
        else:
            message = create_error_response("Hubo un error en el formulario:{form.errors}", 400)
            return render_template('/login.html', form=form, message=message)

#PRIMER REGISTRO, SOLO DEBE VERSE UNA VEZ, O AL REINICIAR VARIABLES DE ENTORNO Y DB
@userRoutes.route("/first_register", methods=['GET', 'POST'])
async def first_register():
    form = FirstRegistrationForm(request.form)
    
    if request.method == 'GET':
        message = create_success_response("Bienvenido al primer registro de administrador", 200)
        return render_template('/first_register.html', form=form, message=message)
    elif request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data 
            email = form.email.data
            password = form.pwd.data
            if firstRegister(username, email, password):
                message = create_success_response("Registrado con éxito, proceda a acceder a la plataforma", 201)
                return redirect(url_for('userRoutes.login')), message
            else:
                message = create_error_response("Escribe bien la información en el registro:{form.errors}", 400)
                return render_template('/first_register.html', message=message)

#FUNCION HOME, REDIRECCIONA A LOGIN O REGISTRO SEGUN LOS CONDICIONALES
@userRoutes.route("/")
async def home():
    is_first_register_made = GlobalSettings.is_first_register_made()
    users_exist = getUsers()

    if is_first_register_made == 'True' and users_exist == 'True':
        return redirect(url_for('userRoutes.login'))
    elif is_first_register_made == 'False' or users_exist == 'False':
        return redirect(url_for('userRoutes.first_register'))

#PASARELA
@userRoutes.route("/pasarela")
@login_required
def pasarela():
    message = create_success_response("Bienvenido a la pasarela", 200)
    return render_template('/pasarela.html', message=message)

#CRUD USUARIOS
@userRoutes.route("/admin/users", methods=['GET'])
@login_required
async def admin_users():
    from models.userModels import Role
    role_choices = [(str(role.id), role.role_name) for role in Role.query.all()]
    
    createuserform = CreateUserForm()
    createuserform.role_id.choices = role_choices

    edituserform = EditUserForm()
    edituserform.role_id.choices = role_choices
    
    deleteuserform = DeleteForm()
    
    users = getUsers()
    return render_template("admin/config_users.html", createuserform=createuserform, edituserform=edituserform, deleteuserform=deleteuserform, usuarios=users, roles=role_choices)

@userRoutes.route("/admin/users", methods=['POST'])
@login_required
async def create_user():
    from models.userModels import Role
    role_choices = [(str(role.id), role.role_name) for role in Role.query.all()]
    createuserform = CreateUserForm()
        
    createuserform.role_id.choices = role_choices  

    if createuserform.validate_on_submit():
        username = createuserform.username.data
        email = createuserform.email.data
        password = createuserform.pwd.data
        role_id = createuserform.role_id.data
        if createUser(username, email, password, role_id):
            message = create_success_response("Usuario creado!", 200)
            return redirect(url_for('userRoutes.admin_users')), message
    else:
        message = create_error_response("Hubo un error en el formulario:{createuserform.errors}", 400)
        return redirect(url_for('userRoutes.admin_users')), message

@userRoutes.route("/admin/users/<int:_id>", methods=['POST'])
@login_required
async def update_user(_id):                                                          
    user = getUserByID(_id)
    edituserform = EditUserForm(obj=user)
    
    if edituserform.validate_on_submit():
        username = edituserform.username.data
        email = edituserform.email.data
        role_id = edituserform.role_id.data
        if updateUser(_id, username, email, role_id):
            message = create_success_response("Usuario actualizado", 200)
            return redirect(url_for('userRoutes.admin_users')), message
        else:
            message = create_error_response("Hubo un error en el formulario: {edituserform.errors}", 400)
            return redirect(url_for('userRoutes.admin_users')), message

@userRoutes.route("/admin/users/delete_<int:_id>", methods=['POST'])
@login_required
async def delete_user(_id):
    deleteuserform = DeleteForm()
    if deleteuserform.validate_on_submit() and deleteUser(_id):
        message = create_success_response("Usuario eliminado", 200)
        return redirect(url_for('userRoutes.admin_users')), message
    else:
        message = create_error_response(f"Hubo un error al eliminar el usuario:{deleteuserform.errors}", 400)
        return redirect(url_for('userRoutes.admin_users')), message

@userRoutes.route("/logout")
@login_required
async def logout():
    logout_user()
    message = create_success_response(f'Ha cerrado sesión: {current_user.email}', 200)
    return redirect('/login'), message