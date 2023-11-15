# Mini-Database Management System, made with Flask

#### Flask web-app to visualize industrial oriented processes, such as PLC variables from sawmill machineries, saved inside MySQL Databases.
Extesions used in this project:
- SQL ORM: [Flask-SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- User auth: [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- Form integration & security: [Flask-WTF](https://flask-login.readthedocs.io/en/latest/)
- Encrypting and hashing: [Flask-Bcrypt](https://flask-login.readthedocs.io/en/latest/)
- Socket and Push events: [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest)
- Email-validator for WTForms: [email-validator](https://pypi.org/project/email-validator/)
- Asynchrounous functions and calls: [asyncio](https://docs.python.org/3/library/asyncio.html#module-asyncio)
- Package version control and environment manager for Python: [Pip-env](https://pipenv.readthedocs.io/es/latest/)
- Environment configuration for Flask app: [python-dotenv](https://pypi.org/project/python-dotenv/)
- Testing library: [PyTest]()

## Setting up the app
First of all, you need to download the app, using:
```
$ git clone https://github.com/MatiasSeb/AserraderosDashboardFlask.git"
```
Inside of the folder where you want the app to be.
Once you've downloaded/cloned it, you'll need to enter the terminal inside the app folder, to initialize pipenv shell, which will initialize the environment for the app, and install the packages needed for the app, using:
```
$ pipenv shell
$ pipenv install
```
After installing the packages, you can run using the commands:

````
flask run
````
or

