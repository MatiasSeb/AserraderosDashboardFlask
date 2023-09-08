from config.extensions import db
from datetime import datetime
Base = db.Model

class Databases(Base):
    __tablename__ = 'databases'
    
    _id = db.Column(db.Integer, primary_key=True)
    connection_name = db.Column(db.String(64), nullable=False)
    conn_username = db.Column(db.String(64), nullable=False)
    conn_ip = db.Column(db.String(64), nullable=False)
    conn_port = db.Column(db.String(4), nullable=False)
    conn_dbname = db.Column(db.String(64), nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, connection_name, conn_username, conn_ip, conn_port, conn_dbname):
        self.connection_name = connection_name
        self.conn_username = conn_username
        self.conn_ip = conn_ip
        self.conn_port = conn_port
        self.conn_dbname = conn_dbname    
    
    def __repr__(self):
        return '<Databases &r>' % self.connection_name
    
    def getConnById(self, _id):
        conn = Databases.query.filter_by(self_id=_id).first()
        if conn:
            return conn
        else:
            raise ValueError(f'No database found with ID {_id}')