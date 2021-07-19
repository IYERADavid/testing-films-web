from src.app import app, db, mail, ts
from src.forms import Signupform, Signinform, Video_uploader, Update_video, \
    Reset_password, New_password, Profile
from src.storage.database_client import UserDatabaseClient
from flask import render_template, redirect, url_for, flash, session, request, \
    send_file, send_from_directory
from functools import wraps
from werkzeug.utils import secure_filename
from flask_mail import Message
from src.settings import get_env



# This is signin_required decorator for verifying
#  if a user has logged in
def signin_required(func):
    @wraps(func)
    def secure_function(*args, **kwargs):
        if 'user_id' in session:
            return func(*args,**kwargs)
        url_value = request.url
        if "/signout" in url_value:
            flash(
                "You are no longer signed in so you can't signout \
                instead signin first")
            return redirect(url_for('index'))

        elif get_env("admin_route") in url_value:
            flash(
                u'You must login to continue on {}'.format(url_value),
                'signin_required')
            return redirect(url_for('admin_login', next_url=url_value))

        flash(
            u'You must signin to continue on {}'.format(url_value),
            'signin_required')
        return redirect(url_for('signin', next_url=url_value))

    return secure_function


# This is admin_role_required decorator for verifying
#  if a user has admin role
def admin_role_required(func):
    @wraps(func)
    def secure_function(*args, **kwargs):
        user_id = session.get('user_id', None)
        user = UserDatabaseClient.get_user(user_id)
        if UserDatabaseClient.user_has_role(user=user, user_role=get_env("staff_role")):
            return func(*args, **kwargs)

        flash(u'You are not allowed to visit this page {}'.format(request.url), 'page_error')
        return redirect(url_for('home'))

    return secure_function


# This is Super_admin_role_required decorator for verifying
#  if a user has Super_admin role
def Super_admin_role_required(func):
    @wraps(func)
    def secure_function(*args, **kwargs):
        user_id = session.get('user_id', None)
        user = UserDatabaseClient.get_user(user_id)
        if UserDatabaseClient.user_has_role(user=user, user_role=get_env("super_role")):
            return func(*args, **kwargs)
        elif UserDatabaseClient.user_has_role(user=user, user_role=get_env("staff_role")):
            flash(
                u'You are not allowed to visit this page {}'.format(request.url),
                'page_error')
            return redirect(url_for('admin_profile'))

        flash(u'You are not allowed to visit this page {}'.format(request.url), 'page_error')
        return redirect(url_for('home'))

    return secure_function


@app.before_first_request
def create_admin():
    UserDatabaseClient.create_db_and_admin()


# This route it is home for all users available for every one
# espicially those who visit us for the first time or those
# who have not logged in. 
@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

#This route it is home page for only users who logged in.
@app.route('/home', methods=['GET', 'POST'])
@signin_required
def home():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    if request.method == 'POST':
        video_name = request.form['movie_name']
        videos = UserDatabaseClient.videos_with_name(video_name)
        return render_template('home.html', user=user,videos=videos)

    videos = UserDatabaseClient.uploaded_videos()
    return render_template('home.html', user=user,videos=videos)

@app.route('/home/profile', methods=['GET','POST'])
@signin_required
def user_profile():
    form = Profile()
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    if form.validate_on_submit():
        profile = form.profile_photo.data
        profile_name = secure_filename(profile.filename)
        UserDatabaseClient.update_profile(
            user_id=user_id,profile_name=profile_name,profile=profile)
        flash('Profile picture updated successfully',"update_success")
        return redirect(url_for('user_profile'))

    return render_template('user_profile.html', form=form,user=user)


@app.route('/delete/profile')
def remove_profile():
    user_id = session.get('user_id', None)
    UserDatabaseClient.remove_profile(user_id=user_id)
    flash('Profile picture deleted successfully',"delete_success")
    return redirect(url_for('user_profile'))



@app.route('/home/watch-movies-Genre-<name>', methods=['GET', 'POST'])
@signin_required
def videos_genre(name):
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    if request.method == 'POST':
        video_name = request.form['movie_name']
        videos = UserDatabaseClient.videos_with_name(video_name)
        return render_template('genres.html', user=user,videos=videos)

    videos = UserDatabaseClient.videos_with_genre(name)
    return render_template('genres.html', user=user, videos=videos)

@app.route('/home/watch-movies-Year-<number>', methods=['GET', 'POST'])
@signin_required
def videos_year(number):
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    if request.method == 'POST':
        video_name = request.form['movie_name']
        videos = UserDatabaseClient.videos_with_name(video_name)
        return render_template('years.html', user=user,videos=videos)

    videos = UserDatabaseClient.videos_with_year(number)
    return render_template('years.html', user=user, videos=videos)

@app.route('/home/watch-movies-language-<name>', methods=['GET', 'POST'])
@signin_required
def videos_language(name):
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    if request.method == 'POST':
        video_name = request.form['movie_name']
        videos = UserDatabaseClient.videos_with_name(video_name)
        return render_template('languages.html', user=user,videos=videos)

    videos = UserDatabaseClient.videos_with_language(name)
    return render_template('languages.html', user=user, videos=videos)

@app.route('/movie/<video_id>')
@signin_required
def single_video(video_id):
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    video = UserDatabaseClient.get_video(video_id)
    if video:
        return render_template('video.html',video=video, user=user)
    flash('The video you are trying to access does not exist','invalid_data')
    return redirect(url_for('home'))

@app.route('/recent_movies')
@signin_required
def recent_videos():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    videos = UserDatabaseClient.new_videos()
    return render_template('recent.html', user=user, videos=videos)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signupform()
    if form.validate_on_submit():
        first_name_value = form.first_name_input.data
        last_name_value = form.last_name_input.data
        middle_name_value = form.middle_name_input.data
        email_value = form.email_input.data
        password_value = form.password_input.data

        if UserDatabaseClient.check_if_email_exists(email=email_value):
            flash(
                u'Sorry account not created! we already have \
                the email you entered.', 'existing_email')
            return redirect(url_for('signup'))

        user = UserDatabaseClient.add_new_user(
            first_name=first_name_value, last_name=last_name_value,
            middle_name=middle_name_value, email=email_value,
            password=password_value)

        UserDatabaseClient.add_user_role(user=user, role=get_env("user_role"))
        flash(
            u'Account successful created for {}'.format(first_name_value),
            'new_user')
        return redirect(url_for('signin'))

    return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = Signinform()
    if form.validate_on_submit():
        email_value = form.email_input.data
        password_value = form.password_input.data
        remember_me_value = form.remember_me_box.data
        next_url_value = form.next_url.data
        user_email = UserDatabaseClient.check_if_email_exists(email=email_value)
        if user_email:
            user = UserDatabaseClient.login_user(
                email=email_value, password=password_value)
            if user:
                session.permanent = remember_me_value
                session['user_id'] = user.user_id
                flash(
                    '{} signed in successful'.format(user.first_name),
                    'user_logged_in')   
                if next_url_value:
                    return redirect(next_url_value)
                return redirect(url_for('home'))

            flash('Your Password is invalid', 'invalid_data')
            return redirect(url_for('signin'))

        flash('Your E-mail is invalid', 'invalid_data')
        return redirect(url_for('signin'))

    return render_template('signin.html', form=form)


@app.route('/signout', methods=['GET'])
@signin_required
def signout():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    session.pop('user_id', None)
    flash(
        u'{} signed out successful \
        '.format(user.first_name),'user_logged_out')
    return redirect(url_for('index'))


@app.route('/reset_password', methods=['GET','POST'])
def change_password():
    form = Reset_password()
    if form.validate_on_submit():
        user_email = form.email.data
        user = UserDatabaseClient.check_if_email_exists(email=user_email)
        if user:
            user_id = UserDatabaseClient.get_user_id(email=user_email)
            token = ts.dumps(user_id, salt=get_env("salt"))
            password_reset_url = url_for('new_password',token=token,_external=True)
            msg = Message(subject="Change password", recipients=[user_email])
            msg.html = render_template('email.html', url=password_reset_url)
            mail.send(msg)
            flash('Check your email inbox to confirm password reset', 'password_reset')
            return render_template('reset_password.html', form=form)
        flash('Your email is invalid', 'invalid_data')
        return redirect(url_for('change_password'))
    return render_template('reset_password.html', form=form)


@app.route("/new_password/<token>", methods=['GET','POST'])
def new_password(token):
    form = New_password()
    try:
        user_id = ts.loads(token, salt=get_env("salt"), max_age=86400)
    except:
        flash(
            'It looks like you password reset request was expired instead you can try again here \
            ', 'token_expired')
        return redirect(url_for('change_password'))
    if form.validate_on_submit():
        password_value = form.password_input.data
        user = UserDatabaseClient.change_password(user_id=user_id,password=password_value)
        flash("{}'s password changed successfull".format(user.first_name),"new_password")
        return redirect(url_for('signin'))
    return render_template('new_password.html', form=form)


@app.route('/delete/account')
@signin_required
def remove_account():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.delete_account(user_id=user_id)
    if not user:
        flash("This account can not be deleted","undeletable_account")
        return redirect(url_for('admin_profile'))
    session.pop('user_id', None)
    flash(
        u"{}'s Acoount successfull deleted \
        ".format(user.first_name),"user_deleted")
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    form = Signinform()
    if form.validate_on_submit():
        email_value = form.email_input.data
        password_value = form.password_input.data
        remember_me_value = form.remember_me_box.data
        next_url_value = form.next_url.data
        user_email = UserDatabaseClient.check_if_email_exists(email=email_value)
        if user_email:
            user = UserDatabaseClient.login_user(
                email=email_value, password=password_value)
            if user:
                if UserDatabaseClient.user_has_role(user=user, user_role="Staff-admin"):
                    session.permanent = remember_me_value
                    session['user_id'] = user.user_id
                    flash(
                        '{} logged in successful'.format(user.first_name),
                        'user_logged_in')
                    if next_url_value:
                        return redirect(next_url_value)
                    return redirect(url_for('admin_profile'))
                flash(
                    u'Dear {} you are not allowed to login here instead try here \
                    '.format(user.first_name), 'admin-login-error')
                return redirect(url_for('signin'))
                
            flash('Your Password is invalid', 'invalid_data')
            return redirect(url_for('admin_login'))

        flash('Your E-mail is invalid', 'invalid_data')
        return redirect(url_for('admin_login'))

    return render_template('admin_login.html', form=form)

@app.route('/admin/home')
@signin_required
@Super_admin_role_required
def admin_home():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    five_videos = UserDatabaseClient.five_recent_videos()
    five_accounts = UserDatabaseClient.five_recent_accounts()
    return render_template('admin_home.html', videos=five_videos,user=user, users=five_accounts)

@app.route('/admin/create_staff_admin', methods=['GET', 'POST'])
@signin_required
@Super_admin_role_required
def new_staff_admin():
    form = Signupform()
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)

    if form.validate_on_submit():
        first_name_value = form.first_name_input.data
        last_name_value = form.last_name_input.data
        middle_name_value = form.middle_name_input.data
        email_value = form.email_input.data
        password_value = form.password_input.data

        if UserDatabaseClient.check_if_email_exists(email=email_value):
            flash(
                u'Sorry account not created! we already have \
                the email you entered.', 'existing_email')
            return redirect(url_for('new_staff_admin'))

        user = UserDatabaseClient.add_new_user(
            first_name=first_name_value, last_name=last_name_value,
            middle_name=middle_name_value, email=email_value,
            password=password_value)

        UserDatabaseClient.add_user_role(user=user, role=get_env("staff_role"))
        UserDatabaseClient.add_user_role(user=user, role=get_env("user_role"))
        flash(
            u'Account with staff-admin role successful created for {}'.format(first_name_value),
            'new_user')
        return redirect(url_for('admin_home'))
    return render_template('staff_admin.html', form=form,user=user)


@app.route('/admin/staff_admins')
@signin_required
@Super_admin_role_required
def all_staff_admins():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    staff_admins_info = UserDatabaseClient.all_staff_admins()
    return render_template('users.html', user=user,users=staff_admins_info)

@app.route('/admin/profile',methods=['GET','POST'])
@signin_required
@admin_role_required
def admin_profile():
    form = Profile()
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    if form.validate_on_submit():
        profile = form.profile_photo.data
        profile_name = secure_filename(profile.filename)
        UserDatabaseClient.update_profile(
            user_id=user_id,profile_name=profile_name,profile=profile)
        flash('Profile picture updated successfully')
        return redirect(url_for('admin_profile'))

    return render_template('admin_profile.html', form=form, user=user)

@app.route('/admin/upload', methods=['GET', 'POST'])
@signin_required
@admin_role_required
def upload_video():
    form = Video_uploader()
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)

    if form.validate_on_submit():
        video_name_value = form.video_name.data
        video_description_value = form.video_description.data
        video_year_value = form.video_year.data
        video_genre_value = form.video_genre.data
        video_language_value = form.video_language.data
        video_file_value = form.video_file.data
        video_photo_value = form.video_photo.data
        video_photo = secure_filename(video_photo_value.filename)
        video_filename = secure_filename(video_file_value.filename)

        UserDatabaseClient.add_new_video(
            video_name=video_name_value,video_description=video_description_value,
            video_photo=video_photo,photo_file=video_photo_value,
            video_filename=video_filename,video_file=video_file_value,
            video_year=video_year_value,video_genre=video_genre_value,
            video_language=video_language_value)
        flash('{} uploaded successfull'.format(video_name_value),'upload-success')
        return redirect(url_for('upload_video'))

    return render_template('upload.html', form=form, user=user)


@app.route('/admin/videos', methods=['GET'])
@signin_required
@admin_role_required
def videos_uploaded():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    videos_info = UserDatabaseClient.uploaded_videos()
    return render_template('videos.html',videos=videos_info, user=user)

@app.route('/admin/videos/update_or_delete/<filename>', methods=['GET','POST'])
@signin_required
@admin_role_required
def update_video(filename):
    form = Update_video()
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    video = UserDatabaseClient.check_if_video_exist(filename)
    if video:
        video_data = UserDatabaseClient.show_video_info(filename)
        if form.validate_on_submit():
            video_name_value = form.video_name.data
            video_description_value = form.video_description.data
            video_year_value = form.video_year.data
            video_genre_value = form.video_genre.data
            video_language_value = form.video_language.data

            video_info = UserDatabaseClient.update_video(
                video_filename=filename,video_name=video_name_value,
                video_description=video_description_value,video_year=video_year_value,
                video_genre=video_genre_value, video_language=video_language_value)
            filename = video_info.video_filename
            flash('video updated successfull','video_updated')
            return redirect(url_for('update_video', filename=filename))

        return render_template('update.html', video=video_data, form=form,user=user)

    flash('Video not found','video_update_error')
    return redirect(url_for('videos_uploaded'))


@app.route('/admin/videos/delete/<filename>')
@signin_required
@admin_role_required
def delete_video(filename):
    video = UserDatabaseClient.check_if_video_exist(filename)
    if video:
        deleted_video = UserDatabaseClient.delete_video(video_filename=filename)
        flash('{} deleted successfull'.format(deleted_video.video_name),'video_deleted')
        return redirect(url_for('videos_uploaded'))

    flash('Video not found','video_delete_error')
    return redirect(url_for('videos_uploaded'))


@app.route('/profile/view')
@signin_required
def view_profile():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    if user.profile_picture:
        return send_from_directory(app.config["UPLOAD_FOLDER"], user.profile_picture)

    return send_from_directory(app.config["UPLOAD_FOLDER"], "default.png")



@app.route('/view_file/<name>')
@signin_required
def view_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/admin/users', methods=['GET','POST'])
@signin_required
@Super_admin_role_required
def all_users():
    user_id = session.get('user_id', None)
    user = UserDatabaseClient.get_user(user_id)
    users_info = UserDatabaseClient.all_users()
    return render_template('users.html', users=users_info, user=user,end_user=True)


if __name__ == "__main__":
    app.run(debug=True)
