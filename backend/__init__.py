from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path
import os

"""
These object can be used throughout project.
1.) Objects from this file can be included in many blueprints
2.) Isolating these object definitions avoids duplication and circular dependencies
"""

# Setup of key Flask object (app)
app = Flask(__name__)
# Setup SQLAlchemy object and properties for the database (db)
dbURI = 'sqlite:///' + os.path.join(os.getcwd(),'backend', 'volumes', 'users.db')
print(dbURI)
project_path = Path.cwd().as_posix()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.secret_key = "8i2VvxY*%voI$hMdxrdj^09I!c4&Z9*r"
db = SQLAlchemy(app)
Migrate(app, db)

# Set up things for authentication
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'  # Set the login view endpoint

# Images storage
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # maximum size of uploaded content
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']  # supported file types
app.config['UPLOAD_FOLDER'] = 'volumes/uploads/'  # location of user uploaded content