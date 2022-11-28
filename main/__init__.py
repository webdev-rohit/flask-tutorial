from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ba25031422bb4953a617046acf46488a'  # this secret key in our app will prevent any kind of external attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # for development purposes we're using a simple file in our machine as a DB, generally in prod, you'd use MySQL, Postgres, etc. Also, here ///means relative path from the current directory, so this statement should create a site.db file in the current directory and use it as the URI to store data
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from main import routes