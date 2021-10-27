# Every level/folder of a Python application has an __init__.py file. The purpose of this file is to connect the levels
# of the app to each other. 

from mongoengine import *
from flask import Flask
import os
from flask_moment import Moment
import base64
from flask_login import LoginManager

app = Flask(__name__)
app.jinja_options['extensions'].append('jinja2.ext.do')
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or os.urandom(20)

connect("capstone", host=f"{os.environ.get('mongodb_host')}/capstone?retryWrites=true&w=majority")
moment = Moment(app)

login = LoginManager(app)
login.login_view = 'login'

def base64encode(img):
    image = base64.b64encode(img)
    image = image.decode('utf-8')
    return image

app.jinja_env.globals.update(base64encode=base64encode)

from .routes import *