import unittest
from index import create_app
from models.userModels import User
from extensions import db
from forms.forms import FirstRegistrationForm, LoginForm

class AppTestCase(unittest.TestCase):
    #setting up the tests for my app
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        
        self.app.config['SQLALCHEMY_DATABASE_URI'] = ''
        self.db = db
        self.db.init_app(self.app)
        
        with self.app.app_context():
            self.db.create_all()
            test_user = User(email='test@test.com')
            test_user.generate_password('testpass')
            self.db.session.add(test_user)
            self.db.session.commit()
    
    #unit test n°1-5
    #1 test for home page
    def testHomePage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    #2 test for register page if home validation gives this page
    def testFirstRegister(self):
        response = self.client.get('/first_register')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/first_register', data={
            'email': 'admin@test.com',
            'password': 'admintest'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    #3 test for login page if home validation gives this page
    def testLogin(self):
        response = self.client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'adminpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Inicio de sesión exitoso', response.data)
        
        response = self.client.get('/pasarela')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bienvenido a la pasarela', response.data)
        
        response = self.client.get('/platform')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Plataforma de visualización', response.data)