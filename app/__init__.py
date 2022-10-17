'''
an init file is required for this folder to be considered as a module
'''
import os
from flask import Flask

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)

# Variable used to refer to templates directory
templates = os.path.join(
    package_dir, "templates"
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

# Temporary for testing, add proper secret key in .env file later
app.config['SECRET_KEY'] = "UhzAQJY9PH"
app.app_context().push()