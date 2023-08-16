from flask import Blueprint, render_template, Response, request, redirect, url_for, flash
from config.extensions import login_manager
from controllers.userController import *
from flask_login import login_required
from forms.forms import FirstRegistrationForm, LoginForm, CreateUserForm, EditUserForm

userRoutes = Blueprint('userRoutes', __name__)

@login_manager.user_loader
def load_user(_id):
    from models.userModels import User
    return User.query.get(_id)

#RUTAS APLICACIÓN FLASK
@userRoutes.route("/")
def home():
    from models.settingModels import GlobalSettings
    from models.userModels import User
    registerform = FirstRegistrationForm()
    loginform = LoginForm()
    
    if GlobalSettings.is_first_register_made() == 'True':
        return render_template('/login.html', form=loginform)
    if GlobalSettings.is_first_register_made() == 'False':
        return render_template('/first_register.html', form=registerform)
    else:
        return 404

#PRIMER REGISTRO, SOLO DEBE VERSE UNA VEZ, O AL REINICIAR LA APP
@userRoutes.route("/first_register", methods=['GET','POST'])
def first_register():
    form = FirstRegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('/first_register.html', form=form)
    if request.method == 'POST':
        username = form.username.data 
        email = form.email.data
        password = form.pwd.data
        if form.validate_on_submit() and firstRegister(username, email, password):
            return redirect('/login')
        else: 
            return Response('Escribe bien la información en el registro', status=400)

#LOGIN USUARIOS
@userRoutes.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('/login.html', form=form)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pwd']
        if form.validate_on_submit():
            return loginUser(email, password)
        else:
            print(form.errors)
            return render_template('/login.html', form=form)

#PASARELA
@userRoutes.route("/pasarela")
@login_required
def pasarela():
    return render_template('/pasarela.html')

#CRUD USUARIOS
@userRoutes.route("/admin/users", methods=['GET'])
@login_required
def admin_users():
    from models.userModels import Role
    role_choices = [(str(role.id), role.role_name) for role in Role.query.all()]
    
    createuserform = CreateUserForm()
    createuserform.role_id.choices = role_choices

    edituserform = EditUserForm()
    edituserform.role_id.choices = role_choices
    
    users = getUsers()
    return render_template("admin_config_users.html", createuserform=createuserform, edituserform=edituserform, usuarios=users, roles=role_choices)

@userRoutes.route("/admin/users", methods=['POST'])
@login_required
def create_user():    
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
            flash('Usuario creado!')
            return redirect(url_for('userRoutes.admin_users'))
    else:
        print(createuserform.errors)
        flash("Hubo un error en el formulario")
    
    return redirect(url_for('userRoutes.admin_users'))

@userRoutes.route("/admin/users/<int:_id>", methods=['GET', 'POST'])
@login_required
def update_user(_id):
    from models.userModels import User, Role                                                            
    user = User.query.get_or_404(_id)
    role_choices = [(str(role.id), role.role_name) for role in Role.query.all()]
    edituserform = EditUserForm(obj=user) 
    edituserform.role_id.choices = role_choices
    
    if request.method == 'POST' and edituserform.validate_on_submit():
        username = edituserform.username.data
        email = edituserform.email.data
        password = edituserform.pwd.data
        role_id = edituserform.role_id.data
        if updateUser(_id, username, email, password, role_id):
            return redirect(url_for('userRoutes.admin_users'))
        else:
            print(edituserform.errors)
    print(edituserform.errors)
    return redirect(url_for('userRoutes.admin_users'))

@userRoutes.route("/admin/users/<int:_id>", methods=['GET', 'POST'])
@login_required
def delete_user(_id):
    if deleteUser(_id):
        flash('Usuario eliminado')
    else:
        flash('Hubo un error al eliminar el usuario')
    return redirect(url_for('admin_users'))


@userRoutes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')