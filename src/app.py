import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.autoversion import Autoversion
from datetime import timedelta

app = Flask(__name__)
# TODO add a function to retrieve environment variables
app.config['SECRET_KEY'] = "ckkkkkkkkkkfigigigigifidifigjbjgj"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../storage/database.db'
basedir = os.path.abspath(os.path.dirname(__file__))
upload_forder = basedir + "/storage/uploads/"
app.config['UPLOAD_FOLDER'] = upload_forder
app.autoversion = True
Autoversion(app)
app.permanent_session_lifetime = timedelta(days=30)
db = SQLAlchemy(app)
