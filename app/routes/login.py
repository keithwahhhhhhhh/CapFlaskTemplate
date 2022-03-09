# These are the routes for logging in a a user and dealing with passwords

from flask_login.utils import login_required
from app import app, login
from werkzeug.urls import url_parse 
from flask import render_template, redirect, flash, url_for, request
from app.classes.data import User
from app.classes.forms import LoginForm, RegistrationForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user
import mongoengine.errors
from app.classes.forms import ResetPasswordRequestForm
from .mail import send_email

# This function is called by other functions to load the current user in to memory
@login.user_loader
def load_user(id):
    try:
        return User.objects.get(pk=id)
    except mongoengine.errors.DoesNotExist:
        flash("Something strange has happened. This user doesn't exist. Please click logout.")
        return redirect(url_for('index'))

# This is the route that a user uses to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # this if statement can be really useful to see if the user that is requesting this
    # page is currently loggedin 
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.objects.get(username=form.username.data)
        except mongoengine.errors.DoesNotExist:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Logout route and function
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Route and function to register a new account
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser = User(
            username=form.username.data, 
            fname=form.fname.data,
            lname=form.lname.data,
            email=form.email.data
            )
        newUser.save()
        newUser.set_password(form.password.data)
        newUser.save()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

# The following functions are for password reset
# This is a helper function that sends a password reset email to a user who has requested
# This funtion does not have a route and is called by other functions.
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Capstone] Reset Your Password',
               sender='swright@ousd.org',
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

# This is the password reset route and function. This function is called when the 
# user requests a password reset
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    try:
        user = User.verify_reset_password_token(token)
    except mongoengine.errors.DoesNotExist:
        flash("I was unable to reset your password.")
        return redirect(url_for('index'))
    else:
        if not user:
            flash("I was unable to reset your password.")
            return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.save()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        try:
            user = User.objects.get(email=form.email.data)
        except mongoengine.errors.DoesNotExist:
            flash(f"I was unable to find a user with email {form.email.data}.")
            return redirect(url_for('index'))
        else:
            if user:
                send_password_reset_email(user)
                flash('Check your email for the instructions to reset your password')
            else:
                flash("Sorry, I was unable to find the user to send the reset email. Please try again.")
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',title='Reset Password', form=form)
