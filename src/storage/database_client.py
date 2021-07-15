import os
from src.app import db,app
from src.storage.database_tables import User, Role, Video, roles_users
from passlib.hash import sha256_crypt


class UserDatabaseClient:

    def create_db_and_admin():
        db.create_all()
        def add_role_available(name, description):
            role = Role(name=name, description=description)
            db.session.add(role)
        add_role_available(name="Super-admin",description="head_of_adminstration")
        add_role_available(name="Staff-admin",description="member_of_adminstration")
        add_role_available(name="End-user",description="client_or_user")
        hashed_password = sha256_crypt.encrypt("testing")
        new_user = User(
            first_name="iyera", last_name="david", middle_name="fred",
            email="testing@gmail.com", password=hashed_password)
        db.session.add(new_user)
        def add_user_role(user, role):
            user_role = Role.query.filter_by(name=role).one()
            user_role.users.append(user)
        add_user_role(user=new_user, role="Super-admin")
        add_user_role(user=new_user, role="Staff-admin")
        add_user_role(user=new_user, role="End-user")
        db.session.commit()
        return new_user

    @staticmethod
    def get_user(id):
        user = User.query.filter_by(user_id=id).one()
        return user
    @staticmethod
    def get_video(video_id):
        video = Video.query.filter_by(video_id=video_id).one_or_none()
        return video


    # Create add_new_user static method
    # This function add a new user to the database
    @staticmethod
    def add_new_user(
            first_name, last_name, middle_name, email, password):
        # Here hashed_password equal to hashed user password
        hashed_password = sha256_crypt.encrypt(password)
        new_user = User(
            first_name=first_name, last_name=last_name,
            middle_name=middle_name, email=email,
            password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def add_user_role(user, role):
        user_role = Role.query.filter_by(name=role).one()
        user_role.users.append(user)
        db.session.commit()
        return user_role

    # This function checks if we already have the user email he/she entered
    # and return true if we have the email and return false if we don't have
    # the email.
    @staticmethod
    def check_if_email_exists(email):
        user = User.query.filter_by(email=email).scalar() is not None
        return user

    # Create user_login static method
    # This function find user in database and return user_object,
    # if no user found it return none
    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).one()
        if sha256_crypt.verify(password, user.password):
            return user
        return None


    @staticmethod
    def add_new_video(
        video_name,video_description,video_photo,photo_file,video_filename,
        video_file,video_year,video_genre,video_language):
        new_video = Video(
            video_name=video_name,video_description=video_description,
            video_photo=video_photo,video_filename=video_filename,
            video_year=video_year,video_genre=video_genre,video_language=video_language)
        photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_photo))
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
        db.session.add(new_video)
        db.session.commit()
        return new_video

    @staticmethod
    def check_if_video_exist(filename):
        video = Video.query.filter_by(video_filename=filename).scalar() is not None
        return video

    @staticmethod
    def show_video_info(filename):
        video_info = Video.query.filter_by(video_filename=filename).one()
        return video_info

    @staticmethod
    def update_video(
        video_filename,video_name, video_description,video_genre,video_year,
        video_language):
        video_info = Video.query.filter_by(video_filename=video_filename).one()
        video_info.video_name = video_name
        video_info.video_description = video_description
        video_info.video_genre = video_genre
        video_info.video_year = video_year
        video_info.video_language = video_language
        db.session.commit()
        return video_info

    @staticmethod
    def delete_video(video_filename):
        video = Video.query.filter_by(video_filename=video_filename).one()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], video.video_filename))
        db.session.delete(video)
        db.session.commit()
        return video

    @staticmethod
    def uploaded_videos():
        all_videos_info = Video.query.order_by(Video.video_id.desc())
        return all_videos_info
    

    # this function query videos that have genre passed in argument
    # and return them in descending order
    @staticmethod
    def videos_with_genre(name):
        all_videos_info = Video.query.filter_by(video_genre=name).all()
        return all_videos_info

    @staticmethod
    def videos_with_year(number):
        number = int(number)
        all_videos_info = Video.query.filter_by(video_year=number).all()
        return all_videos_info

    @staticmethod
    def videos_with_language(name):
        all_videos_info = Video.query.filter_by(video_language=name).all()
        return all_videos_info

    @staticmethod
    def videos_with_name(name):
        all_videos_info = Video.query.filter_by(video_name=name).all()
        return all_videos_info

    # this function query users that have End-user role only
    # and return them in descending order
    @staticmethod
    def all_users():
        all_users = []
        users_info = User.query.order_by(User.user_id.desc())
        for user_info in users_info:
            if len(user_info.roles) == 1:
                all_users.append(user_info)
        return all_users
            

    @staticmethod
    def five_recent_videos():
        videos = Video.query.order_by(Video.video_id.desc())
        five_videos = videos.limit(5)
        return five_videos

    @staticmethod
    def five_recent_accounts():
        accounts = User.query.order_by(User.user_id.desc())
        five_accounts = accounts.limit(5)
        return five_accounts

    @staticmethod
    def user_has_role(user,user_role):
        for role in user.roles:
            if role.name == user_role:
                return role
        return None

    # this function query users that have Staff-admin and End-user roles
    # and return them in descending order
    @staticmethod
    def all_staff_admins():
        all_staff_admins = []
        users_info = User.query.order_by(User.user_id.desc())
        for user_info in users_info:
            if len(user_info.roles) == 2:
                all_staff_admins.append(user_info)
        return all_staff_admins
        
    @staticmethod
    def new_videos():
        all_videos_info = Video.query.order_by(Video.video_year.desc())
        twenty_videos_info = all_videos_info.limit(20) 
        return twenty_videos_info
