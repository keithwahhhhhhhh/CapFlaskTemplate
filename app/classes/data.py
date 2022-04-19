from app import app
from flask import flash
from flask_login import UserMixin
from mongoengine import FileField, EmailField, StringField, ReferenceField, DateTimeField, CASCADE
from flask_mongoengine import Document
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt
import jwt
from time import time
#from bson.objectid import ObjectId

class User(UserMixin, Document):
    username = StringField()
    password_hash = StringField()
    fname = StringField()
    lname = StringField()
    email = EmailField()
    image = FileField()
    role = StringField()
    mascot = StringField()
       
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        id=str(self.id)
        return jwt.encode({'reset_password': id, 'exp': time() + expires_in},app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            flash("Could not verify reset password token.")
            return
        return User.objects.get(pk=id)

class Resource(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    topic = StringField()
    description = StringField()
    restype = StringField()
    link = StringField()
    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class Task(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    sleepTime = StringField()
    work = StringField()
    exercise = StringField()
    exercises = StringField()
    moodRating = StringField()
    meals = StringField()
    meal = StringField()
    thoughts = StringField()
    dental = StringField()
    shower = StringField()

    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class Therapist(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    docName = StringField()
    docEmail = StringField()
    docDescription = StringField()
    gender = StringField()
    ethnicity = StringField()
    age = StringField()
    docLocation = StringField()
    sexuality = StringField()
    timesAvailable = StringField()
    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }
    
class Post(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    subject = StringField()
    content = StringField()
    posttopic = StringField()
    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }


class Comment(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    post = ReferenceField('Post',reverse_delete_rule=CASCADE)
    content = StringField()
    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class resComment(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    post = ReferenceField('Post',reverse_delete_rule=CASCADE)
    resource = ReferenceField('Resource',reverse_delete_rule=CASCADE)
    resDescription = StringField()
    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class TPComment(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    post = ReferenceField('Post',reverse_delete_rule=CASCADE)
    therapist = ReferenceField('Therapist',reverse_delete_rule=CASCADE)
    TPDescription = StringField()
    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }
