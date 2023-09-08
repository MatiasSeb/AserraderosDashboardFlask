from flask_login import login_user

#first register
def firstRegister(username, email, password):
    from models.userModels import User, Role, db
    from models.settingModels import GlobalSettings
    
    if username and email and password:
        hashed_password = User.generate_password(password)
        admin_role = Role.query.filter_by(role_name='Admin').first()
        platform_admin = User(username=username, email=email, password=hashed_password, role_id=admin_role.id)
        db.session.add(platform_admin)
        print(platform_admin)
        db.session.commit()
        GlobalSettings.update_first_admin_registered()
        return True
    return False


#MÉTODOS DE LOS LOGIN
def loginUser(email, password):
    from models.userModels import User
    
    user = User.query.filter_by(email=email).first()
    if user:
        if user.check_password(password):
            login_user(user)
            if user.role_id == 1:
                return 1
            else:
                return 2
        elif not user.check_password(password):
            return 3
    else:
        return 4


#AQUI COMIENZA EL CRUD USUARIOS DE ADMIN CONFIG
#GET USERS
def getUsers():
    from models.userModels import User
    from sqlalchemy.orm import joinedload
    
    users = User.query.options(joinedload(User.role)).all()
    if not users:
        return "User not found", 404
    if users:
        return users

#CREATE USERS
def createUser(username, email, password, role):
    from models.userModels import User, db
    
    if username and email and password and role:
        hashed_pw = User.generate_password(password)
        newUser = User(username, email, password=hashed_pw, role_id=role)
        db.session.add(newUser)
        db.session.commit()
        return newUser
    else: 
        return print('No funciona') 

#UPDATE AN USER
def updateUser(_id, username, email, role):
    from models.userModels import User, db
    
    userToUpdate = User.query.get(_id)
    if not userToUpdate:
        return "User not found", 404
    elif userToUpdate:
        if username and email and role:
            userToUpdate.username = username
            userToUpdate.email = email
            userToUpdate.role_id = role
            db.session.commit()
            return True
        else:
            return False

#DELETE THE USER
def deleteUser(_id):
    from models.userModels import User, db
    
    user = User.query.get_or_404(_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    else:
        return False

