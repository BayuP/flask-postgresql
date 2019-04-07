from flask_wtf import FlaskForm
from wtforms import StringField, Form, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired, Email, Length 


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=-1, max=80, message='You cannot have more than 80 characters')])
    email = StringField('E-Mail', validators=[Email(), Length(min=-1, max=200, message='You cannot have more than 200 characters')])
    address = StringField('Address', validators=[DataRequired(), Length(min=-1, max=200, message='You cannot have more than 200 characters')])

class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(min=-1, max=80, message='You cannot have more than 80 characters')])
    email = StringField('E-Mail', validators=[Email(), Length(min=-1, max=200, message='You cannot have more than 200 characters')])
    address = StringField('Address', validators=[DataRequired(), Length(min=-1, max=200, message='You cannot have more than 200 characters')])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class LoginForm(Form):
    email = StringField('E-Mail', [validators.data_required()])
    password = PasswordField('Password',[validators.DataRequired()])

    
