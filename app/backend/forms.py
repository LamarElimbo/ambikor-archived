from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField('username',  validators=[InputRequired(), Length(max=30)])
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Continue')


class InvitedRegistrationForm(FlaskForm):
    username = StringField('username',  validators=[InputRequired(), Length(max=30)])
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    invitation_code = StringField('invitation_code',  validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Continue')

    
class UpdateAccountForm(FlaskForm):
    username_update = StringField('username',  validators=[InputRequired(), Length(max=30)])
    email_update = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Continue')

    
class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    password_update = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    password_update_verification = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Continue')


class LoginForm(FlaskForm):
    login_email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    login_password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    login_submit = SubmitField('Continue')
    
    
class AdminRegistrationForm(FlaskForm):
    name = StringField('name',  validators=[InputRequired(), Length(max=30)])
    username = StringField('name',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    password_confirmation = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Continue')


class AdminLoginForm(FlaskForm):
    username = StringField('name',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Continue')

    
class TagsForm(FlaskForm):
    tags = StringField('tags')
    submit = SubmitField('Continue')
    
    
class EmailForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])

    
class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])

