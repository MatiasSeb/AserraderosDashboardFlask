from flask import Blueprint, render_template, make_response, request, redirect, url_for, jsonify
from config.extensions import login_manager
from controllers.userController import *
from flask_login import login_required, logout_user, current_user
from forms.forms import FirstRegistrationForm, LoginForm, CreateUserForm, EditUserForm, DeleteForm
import asyncio
userRoutes = Blueprint('userRoutes', __name__)

@login_manager.user_loader
def load_user(_id):
    from models.userModels import User
    return User.query.get(_id)

#RUTAS APLICACIÓN FLASK
@userRoutes.route("/")
async def home():
    from models.settingModels import GlobalSettings
    registerform = FirstRegistrationForm()
    loginform = LoginForm()
    is_first_register_made = await GlobalSettings.is_first_register_made()

    if is_first_register_made == 'True':
        message = "Bienvenido, redirigido al Acceso de usuarios"
        response = make_response(jsonify({'status': 'success', 'message': message}), 200)
        print(response.get_json())
        return render_template('/login.html', form=loginform, message=message)
    elif is_first_register_made == 'False':
        message = "Bienvenido a la plataforma, registrate como administrador para desbloquear el Acceso de usuarios."
        response = make_response(jsonify({'status': 'success', 'message': message}), 200)
        print(response.get_json())
        return render_template('/first_register.html', form=registerform, message=message)

#PRIMER REGISTRO, SOLO DEBE VERSE UNA VEZ, O AL REINICIAR LA APP
@userRoutes.route("/first_register", methods=['POST'])
async def first_register():
    form = FirstRegistrationForm(request.form)
    if form.validate_on_submit():
        username = form.username.data 
        email = form.email.data
        password = form.pwd.data
        if firstRegister(username, email, password):
            message = "Registrado con éxito, proceda a acceder a la plataforma"
            response = make_response(jsonify({'status': 'success', 'message': message}), 200)
            print(response.get_json())
            return redirect('/login')
        else:
            message = (f'Escribe bien la información en el registro:{form.errors}')
            response = make_response(jsonify({'status': 'error', 'message': message}), 400)
            print(response.get_json())
            return render_template('/first_register.html')

#LOGIN USUARIOS
@userRoutes.route("/login", methods=['GET', 'POST'])
async def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        message = "Bienvenido al acceso de usuarios"
        response = make_response(jsonify(({'status': 'success', 'message': message})), 200)
        print(response.get_json())
        return render_template('/login.html', form=form)
    elif request.method == 'POST':
        email = form.email.data
        password = form.pwd.data
        if form.validate_on_submit():
            login_result = loginUser(email, password)
            if login_result == 1:
                message = "Admin conectado."
                response = make_response(jsonify({'status': 'success', 'message': message}), 200)
                print(response.get_json())
                return redirect(url_for('userRoutes.pasarela'))
            elif login_result == 2:
                message = "Usuario conectado."
                response = make_response(jsonify({'status': 'success', 'message': message}), 200)
                print(response.get_json())
                return redirect(url_for('platform'))
            elif login_result == 3:
                message = "Contraseña incorrecta"
                response = make_response(jsonify({'status': 'success', 'message': message}), 400)
                print(response.get_json())
                return redirect(url_for('userRoutes.login')) 
            elif login_result == 4:
                message = "Usuario no encontrado."
                response = make_response(jsonify({'status': 'success', 'message': message}), 404)
                print(response.get_json())
                return redirect(url_for('userRoutes.login')) 
        else:
            message = (f"Hubo un error en el formulario:{form.errors}")
            response = make_response(jsonify({'status': 'errors', 'message': message}), 400)
            print(response.get_json())
            return render_template('/login.html', form=form)

#PASARELA
@userRoutes.route("/pasarela")
@login_required
def pasarela():
    message = "Bienvenido a pasarela"
    response = make_response(jsonify({'status': 'success', 'message': message}), 200)
    print(response.get_json())
    return render_template('/pasarela.html')

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
            message = 'Usuario creado!'
            response = make_response(jsonify({'status': 'success', 'message': message}), 200)
            print(response.get_json())
            return redirect(url_for('userRoutes.admin_users'))
    else:
        message = (f"Hubo un error en el formulario:{createuserform.errors}")
        response = make_response(jsonify({'status': 'error', 'message': message}), 400)
        print(response.get_json())
        return redirect(url_for('userRoutes.admin_users'))

@userRoutes.route("/admin/users/<int:_id>", methods=['POST'])
@login_required
async def update_user(_id):
    from models.userModels import User                                                           
    user = User.query.get_or_404(_id)
    edituserform = EditUserForm(obj=user)
    
    if edituserform.validate_on_submit():
        username = edituserform.username.data
        email = edituserform.email.data
        role_id = edituserform.role_id.data
        if updateUser(_id, username, email, role_id):
            message = 'Usuario actualizado'
            response = make_response(jsonify({'status': 'success', 'message': message}), 200)
            print(response.get_json())
            return redirect(url_for('userRoutes.admin_users'))
        else:
            message = (f'Hubo un error en el formulario: {edituserform.errors}')
            response = make_response(jsonify({'status': 'error', 'message': message}), 400)
            print(response.get_json())
            return redirect(url_for('userRoutes.admin_users'))

@userRoutes.route("/admin/users/delete_<int:_id>", methods=['POST'])
@login_required
async def delete_user(_id):
    deleteuserform = DeleteForm()
    if deleteuserform.validate_on_submit():
        if deleteUser(_id):
            message = 'Usuario eliminado'
            response = make_response(jsonify({'status': 'success', 'message': message}), 200)
            print(response.get_json())
            return redirect(url_for('userRoutes.admin_users'))
        else:
            message = (f'Hubo un error al eliminar el usuario:{deleteuserform.errors}')
            response = make_response(jsonify({'status': 'error', 'message': message}), 400)
            print(response.get_json())
            return redirect(url_for('userRoutes.admin_users'))
    else:
        return redirect(url_for('userRoutes.admin_users'))

@userRoutes.route("/logout")
@login_required
async def logout():
    logout_user()
    message = (f'Ha cerrado sesión: {current_user.email}')
    response = make_response(jsonify({'status': 'success', 'message': message}), 200)
    print(response.get_json())
    return redirect('/login')