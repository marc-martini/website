from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError

# form to register the user
class RegisterForm(FlaskForm):
    firstname = StringField('Name', validators=[DataRequired()])

    lastname = StringField('Name', validators=[DataRequired()])

    email = StringField('Email', validators=[Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()])

    password = PasswordField('Password', validators=[ DataRequired(),
            Length(min=6, message='Select a stronger password.')])

    confirm = PasswordField('Confirm Your Password', validators=[ DataRequired(),
            EqualTo('password', message='Passwords must match.')])

    submit = SubmitField('Register')

# from to login user in
class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField('Email', validators=[DataRequired(),
            Email(message='Enter a valid email.')])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log In')

class Stock(FlaskForm):

    symbol = StringField('Stock Symbol', validators=[DataRequired()])

    submit = SubmitField('Request')

class CompStock(FlaskForm):

    symbol1 = StringField('Stock Symbol 1', validators=[DataRequired()])

    symbol2 = StringField('Stock Symbol 2', validators=[DataRequired()])

    symbol3 = StringField('Stock Symbol 3')

    submit = SubmitField('Compare')

# form for user to change password
class ChangePWForm(FlaskForm):

    current_password = PasswordField('Current Password', validators=[ DataRequired(),
            Length(min=6, message='Select a stronger password.')])

    new_password = PasswordField('New Password', validators=[ DataRequired(),
            Length(min=6, message='Select a stronger password.')])

    new_confirm = PasswordField('Confirm Your Password', validators=[ DataRequired(),
            EqualTo('new_password', message='Passwords must match.')])
            
    submit = SubmitField('Change')