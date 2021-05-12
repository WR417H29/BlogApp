from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# config.py -> this stores a class of AppConfig which is used to initialise the app settings
from api.config import AppConfig

app = Flask(__name__)
app.config.from_object(AppConfig)

db = SQLAlchemy(app)
loginManager = LoginManager()
loginManager.init_app(app)
