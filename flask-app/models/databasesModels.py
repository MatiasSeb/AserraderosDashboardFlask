from config.extensions import db
from datetime import datetime
Base = db.Model
from flask_bcrypt import check_password_hash, generate_password_hash

class Databases(Base):
    __tablename__ = 'databases'
    
    _id = db.Column(db.Integer, primary_key=True)
    connection_name = db.Column(db.String(64), nullable=False)
    conn_username = db.Column(db.String(64), nullable=False)
    conn_password = db.Column(db.String(64), nullable=True)
    conn_ip = db.Column(db.String(64), nullable=False)
    conn_port = db.Column(db.String(4), nullable=False)
    conn_dbname = db.Column(db.String(64), nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, connection_name, conn_username, conn_password, conn_ip, conn_port, conn_dbname):
        self.connection_name = connection_name
        self.conn_username = conn_username
        self.conn_password = conn_password
        self.conn_ip = conn_ip
        self.conn_port = conn_port
        self.conn_dbname = conn_dbname    
    
    def __repr__(self):
        return '<Databases &r>' % self.connection_name
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_password(password):
        return generate_password_hash(password)
    