from sqlalchemy.orm import relationship
from app import db, app
from models.userModels import User
Base = db.Model

class GlobalSettings(Base):
    __tablename__ = 'global_settings'
    
    setting_id = db.Column(db.Integer, primary_key=True, index=True)
    setting_name = db.Column(db.String(50), unique=True, nullable=False)
    setting_value = db.Column(db.String(15), nullable=False)
    
    @staticmethod
    def initialize_settings():
        with app.app_context():
            settings = GlobalSettings.query.all()
            
            if not settings:
                #AQUI SE AGREGAN LAS CONFIGURACIONES DE USUARIO Y CONTENIDO
                default_settings = [
                    GlobalSettings(setting_name='chosen_table', setting_value='camara2'),
                    GlobalSettings(setting_name='first_admin_registered', setting_value='False')
                ]
                db.session.add_all(default_settings)
                db.session.commit()
                print ("Configuraciones cargadas")
    
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
            return 'Primer administrador registrado, registro actualizado'
        else:
            first_admin_register.setting_value = 'False'
            db.session.commit()
            return 'aún no se encuentra un administrador registrado.'