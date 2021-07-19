from datetime import datetime
from src.app import db


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.role_id')))

class Role(db.Model):
    role_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(15), unique=True)
    description = db.Column(db.String(50))


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(321), unique=True, nullable=False)
    profile_picture = db.Column(db.String, nullable=True)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))
    creation_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)



class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    video_photo = db.Column(db.String, unique=True, nullable=False)
    video_filename = db.Column(db.String, unique=True, nullable=False)
    video_name = db.Column(db.String(100), nullable=False)
    video_description = db.Column(db.String(3000), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    video_year = db.Column(db.Integer, nullable=False)
    video_genre = db.Column(db.String(30), nullable=False)
    video_language = db.Column(db.String(30), nullable=False)
    video_time_saved = db.Column(db.DateTime, default=datetime.now(), nullable=False)
