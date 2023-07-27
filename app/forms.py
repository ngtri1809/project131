from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired

from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class ComposeForm(FlaskForm):
    recipient = StringField('Recipient', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

    def validate_recipient(self, recipient):
        user = User.query.filter_by(username=recipient.data).first()
        if not user:
            raise ValidationError('User does not exist')

class ChangePasswordForm(FlaskForm): #takes in user's email, new_password they want to have, and submit
    email = StringField('Email', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')


        
class AddFriendForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) #Takees in user's username
    submit = SubmitField('Add Friend')


class updateForm(FlaskForm):
    bio = StringField('Bio') #takes in bio
    update1 = SubmitField('Update Name') 
    name = StringField('Name')  #takes in name
    update2 = SubmitField('Update Bio')