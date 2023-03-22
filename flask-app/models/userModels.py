from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
Base = db.Model


class User(Base, UserMixin):
    __tablename__ = 'users'
    
    _id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    role = relationship("Role", back_populates="users")
    
    def __init__(self, username, email, password, role_id):
        self.username = username
        self.email = email
        self.password = password
        self.role_id = role_id
    
    def get_id(self):
        return self._id
    
    def __repr__(self):
        return f"User('{self.username}'"
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_password_hash(password):
        return generate_password_hash(password)
    
    def is_admin(role_id):
        admin_role = Role.query.filter_by(role_name='Admin').first()
        return role_id==admin_role.id

class Role(Base):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    role_name = db.Column(db.String(15), unique=True, nullable=False)
    
    users = relationship("User", back_populates="role")
    
    @staticmethod
    def seed():
        roles = ['Admin', 'Normal']
        for role in roles:
            if not Role.query.filter_by(role_name=role).first():
                db.session.add(Role(role_name=role))
        db.session.commit()