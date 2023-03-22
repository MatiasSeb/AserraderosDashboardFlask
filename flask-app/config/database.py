from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv
load_dotenv()

#variables from secrets
db_user = os.getenv("DB_USER")
db_pw = os.getenv("DB_PWD")
db_host = os.getenv("DB_HOSTNAME")
db_port = os.getenv("DB_PORT")
db_usersdbname = os.getenv("DB_USERS_DBNAME")
db_datadbname = os.getenv("DB_DATA_DBNAME")


#users
db_url_users = f"mysql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_usersdbname}"

#data
db_url_data = f"mysql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_datadbname}"
engine = create_engine(db_url_data)
metadata = MetaData()
metadata.reflect(bind=engine)
