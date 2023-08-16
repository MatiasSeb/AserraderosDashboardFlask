from config.extensions import db
from datetime import datetime
from sqlalchemy import create_engine
Base = db.Model

class Databases(Base):
    __tablename__ = 'databases'
    id = db.Column(db.Integer, primary_key=True)
    conn_name = db.Column(db.String(64), nullable=False)
    conn_string = db.Column(db.String(256), nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Databases &r>' % self.conn_name