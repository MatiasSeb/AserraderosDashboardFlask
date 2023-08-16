from flask_login import UserMixin
from sqlalchemy.orm import relationship
from config.extensions import db
from flask_bcrypt import check_password_hash, generate_password_hash
Base = db.Model


class User(Base, UserMixin):
    __tablename__ = 'users'
    
    _id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    role = relationship("Role", backref="users")
    
    def __init__(self, username, email, password, role_id):
        self.username = username
        self.email = email
        self.password = password
        self.role_id = role_id
    
    def get_id(self):
        return self._id
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_password(password):
        return generate_password_hash(password)
    
    def is_admin(role_id):        
        admin_role = Role.query.filter_by(role_name='Admin').first()
        return role_id==admin_role.id
    
    def __repr__(self):
        return f"User('{self.username}'"

class Role(Base):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    role_name = db.Column(db.String(15), unique=True, nullable=False)
    
    def __repr__(self):
        return self.role_name
    
    @staticmethod
    def seed():
        roles = ['Admin', 'Normal']
        for role in roles:
            if not Role.query.filter_by(role_name=role).first():
                db.session.add(Role(role_name=role))
        db.session.commit()