from app import app
from flask_login.utils import login_required
from app import app
from flask import render_template, redirect, flash, url_for
from app.classes.data import User
from app.classes.forms import ProfileForm
from flask_login import current_user

@app.route('/myprofile')

@login_required

def myProfile():

    return render_template('profilemy.html')

@app.route('/myprofile/edit', methods=['GET','POST'])

@login_required

def profileEdit():

    form = ProfileForm()

    if form.validate_on_submit():

        currUser = User.objects.get(id=current_user.id)

        currUser.update(
            lname = form.lname.data,
            fname = form.fname.data,
            role = form.role.data,

        )

        if form.image.data:
            if currUser.image:
                currUser.image.delete()
            currUser.image.put(form.image.data, content_type = 'image/jpeg')

            currUser.save()

        return redirect(url_for('myProfile'))

    form.fname.data = current_user.fname
    form.lname.data = current_user.lname
    form.role.data = current_user.role

    return render_template('profileform.html', form=form)
