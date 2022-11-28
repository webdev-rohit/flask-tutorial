# instead of creating form with html where you would need to add a lot of separate validation using js, we'll use flask_wtf which has many inbuilt validation features and is easy to implement

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) # here, since we would want username to be a string type field, we're using Stringfield class. 'Username' is a label, DataRequired() means that it's a required field and we've added length condition saying that username has to be between 2 to 20 chars long only
    email = EmailField('Email', validators=[DataRequired(), Email()]) # here, Email() class will make sure that email entered has proper email format
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=10)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) # here, we want this field to be equal to the password field so EqualTo() class is used here
    submit = SubmitField('Sign Up')

    # these fxns below are to make sure that username and email entered aren't already taken by anyone else before
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # if this line returns None then it'll not satisfy the condition below, if it returns anything else (which means that there actually exists a username in the db with the same username as entered in the registration form) then the condition below will be executed.
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) # here, Email() class will make sure that email entered has proper email format
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me') # here, since it is either Yes or No, we require a BooleanField input which takes True or False values
    submit = SubmitField('Login')

# Note: for email validation support, we had to install email-validator in our virtual env using pip install email-validator
    
    
