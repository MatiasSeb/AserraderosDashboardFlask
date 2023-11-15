from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, HiddenField, widgets
from wtforms.validators import InputRequired, DataRequired, Email, Length, EqualTo, ValidationError, Regexp, Optional
from models.databasesModels import Databases

#USER FORMS
class FirstRegistrationForm(FlaskForm):
    username = StringField(
        'Nombre', 
        validators=[
            DataRequired(), 
            Length(min=8, max=50, message="Ingrese el nombre de usuario"),
            Regexp(
                r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message="El nombre de usuario solo debe ser escrito con letras."
            )
        ]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    pwd = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=20)], widget=widgets.PasswordInput(hide_value=False))
    c_pwd = PasswordField(
        'Confirmar Contraseña', 
        validators=[
            DataRequired(), 
            EqualTo('pwd', message="Las contraseñas deben ser iguales!")
        ]
    )
    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    email = StringField('Ingrese su Email', validators=[DataRequired(), Email()])
    pwd = PasswordField('Ingrese su Contraseña', validators=[DataRequired(), Length(min=8, max=20)], widget=widgets.PasswordInput(hide_value=False))
    submit = SubmitField('Acceder')

class CreateUserForm(FlaskForm):
    username = StringField(
        'Nombre de usuario', 
        validators=[
            DataRequired(), 
            Length(min=8, max=50, message="Ingrese el nombre de usuario"),
            Regexp(
                r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message="Los nombres de usuario solo deben ser escritos con letras."
            )
        ]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    pwd = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=20)], widget=widgets.PasswordInput(hide_value=False))
    c_pwd = PasswordField(
        'Confirmar Contraseña', 
        validators=[
            DataRequired(), 
            EqualTo('pwd', message="Las contraseñas deben ser iguales!")
        ]
    )
    role_id = SelectField('Rol', choices=[], validators=[DataRequired()])
    submit = SubmitField('Crear usuario')

class EditUserForm(FlaskForm):
    username = StringField(
        'Nombre de usuario', 
        validators=[
            DataRequired(), 
            Length(min=8, max=50, message="Ingrese el nombre de usuario"),
            Regexp(
                r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message="Los nombres de usuario solo deben ser escritos con letras."
            )
        ]
    )
    email = StringField('Email del usuario', validators=[DataRequired(), Email()])
    role_id = SelectField('Rol del usuario', choices=[], validators=[DataRequired()])
    submit = SubmitField('Modificar usuario')

#DATABASE FORMS
class CreateDBConnForm(FlaskForm):
    connection_name = StringField(
        'Nombre de conexión', 
        validators=[
            DataRequired(), 
            Length(min=8, max=50, message="Ingrese el nombre de conexión"),
        ]
    )
    conn_username = StringField('Username', validators=[DataRequired()])
    conn_ip = StringField('IP Address', validators=[DataRequired()])
    conn_port = StringField('Port', validators=[DataRequired()])
    conn_dbname = StringField('Database Name', validators=[DataRequired()])
    submit = SubmitField('Crear conexión')

class EditDBConnForm(FlaskForm):
    connection_name = StringField(
        'Nombre de conexión', 
        validators=[
            DataRequired(), 
            Length(min=8, max=50, message="Ingrese el nombre de conexión"),
        ]
    )
    conn_username = StringField('Username', validators=[DataRequired()])
    conn_ip = StringField('IP Address', validators=[DataRequired()])
    conn_port = StringField('Port', validators=[DataRequired()])
    conn_dbname = StringField('Database Name', validators=[DataRequired()])
    submit = SubmitField('Modificar conexión')

class SelectDatabaseForm(FlaskForm):
    selected_conn = SelectField('Credenciales a elegir', choices=[], validators=[DataRequired()])
    db_pwd = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=20)], widget=widgets.PasswordInput(hide_value=False))
    submit = SubmitField('Conectar')

class SelectTableFromDBForm(FlaskForm):
    selected_table = SelectField('Tabla a elegir', choices=[], validators=[DataRequired()])
    submit = SubmitField('Elegir tabla para stremear en tiempo real')
    
#DELETE FORM FOR EVERYTHING
class DeleteForm(FlaskForm):
    class Meta:
        csrf = True
    submit = SubmitField('Eliminar')
