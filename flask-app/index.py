from app import create_app
from models.settingModels import GlobalSettings
from models.userModels import Role

app = create_app()

with app.app_context():
    GlobalSettings.initialize_settings()
    Role.seed()

if __name__ == "__main__":
    app.run(debug=True)