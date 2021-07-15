from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    HiddenField, TextAreaField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired


class Signupform(FlaskForm):
    first_name_input = StringField(
        '',
        validators=[
            InputRequired(message="You must fillout this field!"),
            Length(
                max=24,
                message='Your name must be less than 25 characters!')],
        render_kw={
            'id': 'first_name', 'class': 'form-control',
            'placeholder': 'First name'}
    )
    last_name_input = StringField(
        '',
        validators=[
            InputRequired(message="You must fillout this field!"),
            Length(
                max=24,
                message='Your name must be less than 25 characters!')],
        render_kw={
            'id': 'last_name', 'class': 'form-control',
            'placeholder': 'Last name'}
    )
    middle_name_input = StringField(
        '',
        validators=[
            Length(
                max=14,
                message='Your name must be less than 15 characters!')],
        render_kw={
            'id': 'middle_name', 'class': 'form-control',
            'placeholder': 'Middle name'}
    )
    email_input = StringField(
        '',
        validators=[
            InputRequired(message="You must fillout this field!"),
            Length(
                # Valid email must have the maximum length of 320 characters
                # from
                # https://www.rfc-editor.org/errata/eid1690#:~:text=It%20should%20say%3A-,In%20addition%20to
                # %20restrictions%20on%20syntax%2C%20there%20is%20a%20length,total%20length%20of%20320%20characters.
                max=320,
                message="your email must be less than 321 characters!"),
            email(message='Your email is not valid!')],
        render_kw={
            'id': 'email', 'class': 'form-control',
            'placeholder': 'email'}
    )
    password_input = PasswordField(
        '',
        validators=[
            InputRequired(message="You must fillout this field!"),
            Length(
                min=6,
                message='Your password must be greater than 5 characters')],
        render_kw={
            'id': 'password', 'class': 'form-control',
            'placeholder': 'Password'}
    )
    confirm_password_input = PasswordField(
        '',
        validators=[
            InputRequired(message="You must fillout this field!"),
            EqualTo(
                'password_input',
                message="Your passwords does not match!")],
        render_kw={
            'id': 'confirm_password', 'class': 'form-control',
            'placeholder': 'Re enter password'}
    )
    submit = SubmitField('Signup', render_kw={'class': 'btn btn-info'})


class Signinform(FlaskForm):
    email_input = StringField(
        '',
        validators=[
            InputRequired(message='You must fillout this field!'),
            Length(
                # Valid email must have the maximum length of 320 characters
                # from
                # https://www.rfc-editor.org/errata/eid1690#:~:text=It%20should%20say%3A-,In%20addition%20to
                # %20restrictions%20on%20syntax%2C%20there%20is%20a%20length,total%20length%20of%20320%20characters.
                max=320,
                message="your email must be less than 321 characters!"),
            email(message="your email is not valid")],
        render_kw={
            'id': 'email', 'class': 'login-form-control',
            'placeholder': 'email'}
    )
    password_input = PasswordField(
        '',
        validators=[
            InputRequired(message='You must fillout this field!'),
            Length(
                min=6,
                message='Your password must be greater than 5 characters')],
        render_kw={
            'id': 'password', 'class': 'login-form-control',
            'placeholder': 'Password'}
    )
    remember_me_box = BooleanField('', render_kw={'class': 'remeber_me'})
    next_url = HiddenField('', render_kw={'id': 'next_url', 'value': None})
    submit = SubmitField('signin', render_kw={'class': 'btn btn-success'})


class Video_uploader(FlaskForm):
    video_name =  StringField(
        '',
        validators=[
            InputRequired(message='You must fillout this field!'),
            Length(
                max=99,
                message='Your name must be less than 100 characters!')],
        render_kw={
            'class': 'form-control', 'id': 'video_name',
            'placeholder': 'Video Name'}
    )
    video_description = TextAreaField(
        '',
        validators=[
            InputRequired(message='You must fillout this field!'),
            Length(
                max=2999,
                message='Your description must be less than 3000 characters!')],
        render_kw={
            'class': 'form-control', 'id': 'video_description',
            'placeholder': 'Video Description', 'rows': '5'}
    )
    video_photo = FileField(
        '',
        validators=[
            FileRequired(message='You must fillout this field!'),
            FileAllowed(['jpg', 'png', 'jpeg'], message="un supported format")]
    )
    video_file = FileField(
        '',
        validators=[
            FileRequired(message='You must fillout this field!'),
            FileAllowed(['mp4', 'avi', 'm4a'], message="un supported format")]
    )
    video_year = IntegerField(
        '',
        validators=[
            InputRequired(message='You must fillout this field!'),
            NumberRange(
                min=1600,max=2022,
                message="Video year must be made of 4 digits")],
        render_kw={
            'class': 'form-control', 'id': 'video_year',
            'placeholder': 'eg: 2000'
        }
    )
    video_genre = SelectField(
        '',
        choices=[
            ('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'),
            ('Biography','Biography'), ('Comedy','Comedy'), ('Documentary','Documentary'),
            ('Drama','Drama'), ('Family','Family'), ('Fantasy','Fantasy'), ('Game-show','Game-show'),
            ('History','History'), ('Horror','Horror'),('Music','Music'), ('Mystery','Mystery'),
            ('News','News'), ('Romance','Romance'), ('Sport','Sport'), ('Talk-show','Talk-show'),
            ('War','war'),('Western','Western'),('Adult','Adult')], default='Action'
    )
    video_language = SelectField(
        '',
        choices=[
            ('English','English'), ('French', 'French'), ('Kinyarwanda','Kinyarwanda'),
            ('Italian','Italian'), ('Germany','Germany'), ('Portuguese','Portuguese'),
            ('Chinese','Chinese'), ('Espanol','Esponol'), ('Japanese','Japanese')
        ], default='English'
    )
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-success'})


class Update_video(FlaskForm):
    video_name =  StringField(
        '',
        validators=[
            InputRequired(message='You must fillout this field!'),
            Length(
                max=99,
                message='Your name must be less than 100 characters!')],
        render_kw={
            'type': 'text', 'class': 'form-control', 'id': 'video_name',
            'placeholder': 'Video Name'}
    )
    video_description = TextAreaField(
        '',
        validators=[
            InputRequired(message='You must fillout this field!'),
            Length(
                max=2999,
                message='Your description must be less than 3000 characters!')],
        render_kw={
            'class': 'form-control', 'id': 'video_description', 'rows': '5'}
    )
    video_year = IntegerField(
        '',
        validators=[
            InputRequired(message='You must fillout this field!'),
            NumberRange(
                min=1600,max=2022,
                message="Video year must be made of 4 digits")],
        render_kw={
            'class': 'form-control', 'id': 'video_year',
            'placeholder': 'eg: 2000'
        }
    )
    video_genre = SelectField(
        '',
        choices=[
            ('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'),
            ('Biography','Biography'), ('Comedy','Comedy'), ('Documentary','Documentary'),
            ('Drama','Drama'), ('Family','Family'), ('Fantasy','Fantasy'), ('Game-show','Game-show'),
            ('History','History'), ('Horror','Horror'),('Music','Music'), ('Mystery','Mystery'),
            ('News','News'), ('Romance','Romance'), ('Sport','Sport'), ('Talk-show','Talk-show'),
            ('War','war'),('Western','Western'),('Adult','Adult')], default='Action'
    )
    video_language = SelectField(
        '',
        choices=[
            ('English','English'), ('French', 'French'), ('Kinyarwanda','Kinyarwanda'),
            ('Italian','Italian'), ('Germany','Germany'), ('Portuguese','Portuguese'),
            ('Chinese','Chinese'), ('Espanol','Esponol'), ('Japanese','Japanese')
        ], default='English'
    )
    submit = SubmitField('Update', render_kw={'class': 'btn btn-info'})
