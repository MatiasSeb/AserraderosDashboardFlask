from app import app, db
from models.settingModels import GlobalSettings
from models.userModels import Role

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        GlobalSettings.initialize_settings()
        Role.seed()

    app.run(debug=True)