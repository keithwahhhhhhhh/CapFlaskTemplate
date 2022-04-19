# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from msilib.schema import RadioButton
from flask.app import Flask
from flask import flash
from flask_wtf import FlaskForm
from mongoengine.fields import EmailField
import mongoengine.errors
from wtforms.validators import URL, NumberRange, Email, Optional, InputRequired, ValidationError, DataRequired, EqualTo
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, HiddenField, IntegerField, SelectField, FileField, BooleanField, SelectMultipleField
from app.classes.data import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])  
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        try:
            User.objects.get(username=username.data)
        except mongoengine.errors.DoesNotExist:
            flash(f"{username.data} is available.")
        else:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        try:
            User.objects.get(email=email.data)
        except mongoengine.errors.DoesNotExist:
            flash(f'{email.data} is a unique email address.')
        else:
            raise ValidationError('This email address is already in use. if you have forgotten your credentials you can try to recover your account.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')
    role = SelectField('Role',choices=[("User","User"),("Therapist","Therapist")])
    mascot = SelectField('Mascot',choices=[("Slug","Slug"),("Panther","Panther")])
   
class ResourceForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    description = TextAreaField('Resource', validators=[DataRequired()])
    restype = SelectField('Type',choices=[("Video","Video"),("Article","Article"),("Other","Other")])
    link = TextAreaField('Link', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    sleepTime = SelectField('sleepTime',choices=[("Less than 1 hour","Less than 1 Hour "),("1 Hour","1 Hour"),("2 Hours","2 Hours"),("2 Hours","2 Hours"),("3 Hours","3 Hours"),("4 Hours","4 Hours"),("5 Hours","5 Hours"),("6 Hours","6 Hours"),("7 Hours","7 Hours"),("8 Hours","8 Hours"),("9 Hours","9 Hours"),("10 Hours","10 Hours"),("10+ Hours","10+ Hours")])
    work = SelectField('work',choices=[("All work completed","All work completed"),("Most work completed","Most work completed"),("A good amount of work completed","A good amount of work completed"),("Very little work completed","Very little work completed"),("No work completed","No work completed")])
    exercise = SelectField('exercise',choices=[("Yes","Yes"),("No","No")])
    exercises = TextAreaField('exercises', validators=[DataRequired()])
    moodRating = SelectField('moodRating',choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10")])
    meals = SelectField('meals',choices=[("Breakfast","Breakfast"),("Lunch","Lunch"),("Dinner","Dinner")])
    meal = TextAreaField('Meal', validators=[DataRequired()])
    thoughts = TextAreaField('thoughts', validators=[DataRequired()])
    dental = SelectField('dental',choices=[("Brushed once, no flossing","Brushed once, no flossing"),("Brushed twice, no flossing","Brushed twice, no flossing"),("Brushed once with flossing","Brushed once with flossing"),("Brushed twice with flossing","Brushed twice with flossing"),("Other","Other")])
    shower = SelectField('exercise',choices=[("Yes","Yes"),("No","No")])
    submit = SubmitField('Enter Entry')

class TherapistForm(FlaskForm):
    docName = StringField('docName', validators=[DataRequired()])
    docEmail = StringField('docEmail', validators=[DataRequired()])
    docLocation = StringField('docLocation', validators=[DataRequired()])
    docDescription = TextAreaField('docDescription', validators=[DataRequired()])
    gender = StringField('gender', validators=[DataRequired()])
    ethnicity = StringField('ethnicity', validators=[DataRequired()])
    age = StringField('age', validators=[DataRequired()])
    sexuality = StringField('sexuality', validators=[DataRequired()])
    timesAvailable = StringField('timesAvailable', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Post', validators=[DataRequired()])
    posttopic = StringField('postTopic', validators=[DataRequired()])
    submit = SubmitField('Post')
    
class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class resCommentForm(FlaskForm):
    resDescription = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class TPCommentForm(FlaskForm):
    TPDescription = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')