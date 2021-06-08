from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# config.py -> this stores a class of AppConfig which is used to initialise the app settings
from api.config import AppConfig

app = Flask(__name__)  # creating flask app
app.config.from_object(AppConfig)  # configuring the app

db = SQLAlchemy(app)  # creating a database reference
loginManager = LoginManager()  # creating a login manager
loginManager.init_app(app)  # initialising the login manager with the flask app
