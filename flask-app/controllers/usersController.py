from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.userModels import User, Role
from models.settingModels import GlobalSettings
from app import login_manager, db

usersapi = Blueprint('usersapi', __name__)

@login_manager.user_loader
def load_user(_id):
    return User.query.get(_id)

#RUTAS APLICACIÓN FLASK
@usersapi.route("/")
def home():
    if GlobalSettings.is_first_register_made() == 'True':
        return render_template('/login.html')
    if GlobalSettings.is_first_register_made() == 'False':
        return render_template('/first_register.html')
    else:
        return 404

@usersapi.route("/first_register", methods=['GET','POST'])
def first_register():
    if request.method == 'GET':
        return render_template('/first_register.html')
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = User.generate_password_hash(password)
        admin_role = Role.query.filter_by(role_name='Admin').first()
        new_admin = User(username=username, email=email, password=hashed_password, role_id=admin_role.id)
        db.session.add(new_admin)
        db.session.commit()
        GlobalSettings.update_first_admin_registered()
        return redirect('/login')
    else: 
        return 'te equivocaste en el registro'
    

@usersapi.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            if user.role_id == 1:
                return render_template('/pasarela.html')
            else:
                return render_template('/pasarela.html')
        else:
            flash ("Login again, invalid email or password")
            return redirect('/login')
        


@usersapi.route("/pasarela")
@login_required
def pasarela():
    if not current_user.is_authenticated():
        return render_template(url_for('/login'))
    if User.is_admin(current_user.role_id):
        return render_template('/admin_config_users')
    else:
        return redirect(url_for('/127.0.0.1:8501'))

@usersapi.route("/admin_config_users")
@login_required
def admin_config():
    return render_template('admin_config_users.html')

#AQUI COMIENZA EL CRUD USUARIOS DE ADMIN CONFIG
@usersapi.route("/admin_config/users/<int:user_id>", methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.filter_by(_id=user_id).first()
    if not user:
        return "User not found", 404
    return user.username

@usersapi.route("/admin_config/users/add/<int:user_id>", methods=['POST'])
@login_required
def create_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role_id = request.form['role_id']
    
    hashed_password = User.generate_password_hash(password)
    
    newUser = User(username, email, hashed_password, role_id)
    db.session.add(newUser)
    db.session.commit()
    
    if not newUser:
        return 401
    else:
        flash('success') 
        return redirect(url_for('/admin_config')) and 201

@usersapi.route("/admin_config/users/update/<int:user_id>", methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.filter_by(_id=user_id).first()
    if not user:
        return 404
    if user:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']
        
        hashed_password = User.generate_password_hash(password)
        if username and email and hashed_password and role_id:
            user = User(username, email, hashed_password, role_id)
        else:
            return "te equivocaste en algun dato revisa bien"
        db.session.add(user)
        db.session.commit()
    return flash('success', 'usuario actualizado')

@usersapi.route("/admin_config/users/delete/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(_id=user_id).first()
    if not user:
        return 404
    if user:
        db.session.delete(user)
        db.session.commit()
    else:    
        return  "te equivocaste en algun dato revisa bien"
    return flash('success', 'usuario eliminado')














@usersapi.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))