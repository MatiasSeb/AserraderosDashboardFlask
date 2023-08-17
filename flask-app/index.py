from app import create_app, db
from models.settingModels import GlobalSettings
from models.userModels import Role
from models.databasesModels import Databases

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
        GlobalSettings.initialize_settings()
        Role.seed()

    app.run(debug=True)