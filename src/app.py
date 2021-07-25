import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.autoversion import Autoversion
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail
from src.export_variables import export_envs
from src.settings import get_env

export_envs()

app = Flask(__name__)
# TODO add a function to retrieve environment variables
app.config['SECRET_KEY'] = get_env("secret_key")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = get_env("database_url")
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = get_env("email_username")
app.config['MAIL_PASSWORD'] = get_env("email_password")
app.config['MAIL_DEFAULT_SENDER'] = get_env("email_username")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder = basedir + get_env("uploads_path")
app.config['UPLOAD_FOLDER'] = upload_folder
app.autoversion = True
Autoversion(app)
app.permanent_session_lifetime = timedelta(days=7)
db = SQLAlchemy(app)
mail = Mail(app)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
