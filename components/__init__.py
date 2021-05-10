from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from components.config import AppConfig

app = Flask(__name__)
app.config.from_object(AppConfig)

db = SQLAlchemy(app)
loginManager = LoginManager()
loginManager.init_app(app)
