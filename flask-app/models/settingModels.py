from config.extensions import db
from flask import current_app, make_response, jsonify
from models.userModels import User
from helpers.responses import create_error_response, create_success_response


class GlobalSettings(db.Model):
    __tablename__ = 'global_settings'
    
    setting_id = db.Column(db.Integer, primary_key=True, index=True)
    setting_name = db.Column(db.String(50), unique=True, nullable=False)
    setting_value = db.Column(db.String(15), nullable=False)
    
    @staticmethod
    def initialize_settings():
        with current_app.app_context():
            try:
                settings = GlobalSettings.query.all()
                if not settings:
                    #AQUI SE AGREGAN LAS CONFIGURACIONES DE USUARIO Y CONTENIDO
                    default_settings = [
                        GlobalSettings(setting_name='active_conn', setting_value='None'),
                        GlobalSettings(setting_name='chosen_table', setting_value='None'),
                        GlobalSettings(setting_name='first_admin_registered', setting_value='False'),
                        GlobalSettings(setting_name='is_streaming', setting_value='False')
                    ]
                    db.session.add_all(default_settings)
                    db.session.commit()
                    message = "Configuraciones de la base de datos han sido inicializadas."
                    return print(message)
                elif settings:
                    message = "Base de datos ya configurada."
                    return print(message)
            except Exception as e:
                return print(f"Error inicializando configuraciones: {e}")
                
    def is_first_register_made():
        setting = GlobalSettings.query.filter_by(setting_name='first_admin_registered').first()
        first_register_setting = setting.setting_value
        return first_register_setting

    def update_first_admin_registered():
        first_admin_register = GlobalSettings.query.filter_by(setting_name='first_admin_registered').first()
        verify_adm_and_id = User.query.filter_by(role_id=1).first()
        if verify_adm_and_id is not None:
            first_admin_register.setting_value = 'True'
            db.session.commit()
            return print('Primer administrador registrado, registro actualizado')
        else:
            first_admin_register.setting_value = 'False'
            db.session.commit()
            return print('aún no se encuentra un administrador registrado.')
    
    def is_streaming_data():
        setting = GlobalSettings.query.filter_by(setting_name='is_streaming').first()
        streaming_flag = setting.setting_value
        return streaming_flag
    
    def get_chosen_table():
        query = GlobalSettings.query.filter_by(setting_name='chosen_table').first()
        chosen_table = query.setting_value
        return chosen_table
    
    def chosen_table_update(table):
        setting = GlobalSettings.query.filter_by(setting_name='chosen_table').first()
        if setting:
            setting.setting_value = table
            db.session.commit()
    
    def get_chosen_conn():
        conn = GlobalSettings.query.filter_by(setting_name='active_conn').first()
        chosen_conn = conn.setting_value
        return chosen_conn
    
    def update_chosen_conn(conn_name):
        setting = GlobalSettings.query.filter_by(setting_name='active_conn').first()
        if setting:
            setting.setting_value = conn_name
            db.session.commit()
