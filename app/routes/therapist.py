from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Therapist, TPComment
from app.classes.forms import TherapistForm, TPCommentForm
from flask_login import login_required
import datetime as dt


@app.route('/therapist/list')

@login_required
def therapistList():

    therapists = Therapist.objects()

    return render_template('therapists.html',therapists=therapists)

@app.route('/therapist/<therapistID>')

@login_required
def therapist(therapistID):

    thisTherapist = Therapist.objects.get(id=therapistID)
    TPTheseComments = TPComment.objects(therapist=thisTherapist)
    return render_template('therapist.html',therapist=thisTherapist, TPComments = TPTheseComments)


@app.route('/therapist/delete/<therapistID>')

@login_required
def therapistDelete(therapistID):

    deleteTherapist = Therapist.objects.get(id=therapistID)

    if current_user == deleteTherapist.author:

        deleteTherapist.delete()

        flash('The entry was deleted.')
    else:

        flash("You can't delete an entry you don't own.")

    therapists = Therapist.objects()  
    
    return render_template('therapists.html',therapists=therapists)


@app.route('/therapist/new', methods=['GET', 'POST'])

@login_required

def therapistNew():
    
    form = TherapistForm()

   
    if form.validate_on_submit():

    
        newTherapist = Therapist(
          
            docName = form.docName.data,
            docEmail = form.docEmail.data,
            docLocation = form.docLocation.data,
            docDescription = form.docDescription.data,
            gender = form.gender.data,
            ethnicity = form.ethnicity.data,
            age = form.age.data,
            sexuality = form.sexuality.data,
            timesAvailable = form.timesAvailable.data,
            
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )
        
        newTherapist.save()

        return redirect(url_for('therapist',therapistID=newTherapist.id))


    return render_template('therapistform.html',form=form)



@app.route('/therapist/edit/<taskID>', methods=['GET', 'POST'])
@login_required
def TherapistEdit(therapistID):
    editTherapist = Therapist.objects.get(id=therapistID)

    if current_user != editTherapist.author:
        flash("You can't edit an entry you don't own.")
        return redirect(url_for('therapist',therapistID=therapistID))
    # get the form object
    form = TherapistForm()

    if form.validate_on_submit():

        editTherapist.update(
            docName = form.docName.data,
            docEmail = form.docEmail.data,
            docLocation = form.docLocation.data,
            docDescription = form.docDescription.data,
            gender = form.gender.data,
            ethnicity = form.ethnicity.data,
            age = form.age.data,
            sexuality = form.sexuality.data,
            timesAvailable = form.timesAvailable.data,
            modifydate = dt.datetime.utcnow
        )

        return redirect(url_for('therapist',therapistID=therapistID))

    form.docName.data = editTherapist.docName
    form.docEmail = form.docEmail.data, = editTherapist.docEmail
    form.docLocation = editTherapist.docLocation
    form.docDescription.data = editTherapist.docDescription
    form.gender.data = editTherapist.gender
    form.ethnicity.data = editTherapist.ethnicity
    form.age.data = editTherapist.age
    form.sexuality.data = editTherapist.sexuality
    form.timesAvailable.data = editTherapist.timesAvailable

    return render_template('therapistform.html',form=form)

@app.route('/TPComment/new/<therapistID>', methods=['GET', 'POST'])
@login_required
def TPCommentNew(therapistID):
    therapist = Therapist.objects.get(id=therapistID)
    form = TPCommentForm()
    if form.validate_on_submit():
        newTPComment = TPComment(
            author = current_user.id,
            therapist = therapistID,
            TPDescription = form.TPDescription.data
            
        )
        newTPComment.save()
        return redirect(url_for('therapist',therapistID=therapistID))
    return render_template('therapistsCommentForm.html',form=form,therapist=therapist)

@app.route('/comment/edit/<commentID>', methods=['GET', 'POST'])
@login_required
def TPCommentEdit(TPCommentID):
    TPEditComment = TPComment.objects.get(id=TPCommentID)
    if current_user != TPEditComment.author:
        flash("You can't edit a comment you didn't write.")
        return redirect(url_for('therapist',therapistID=TPEditComment.therapist.id))
    therapist = Therapist.objects.get(id=TPEditComment.therapist.id)
    form = TPCommentForm()
    if form.validate_on_submit():
        TPEditComment.update(
            TPDescription = form.TPDescription.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('therapist',therapistID=TPEditComment.therapist.id))

    form.TPDescription.data = TPEditComment.TPDescription

    return render_template('therapistsCommentForm.html',form=form,therapist=therapist)   

@app.route('/comment/delete/<commentID>')
@login_required
def TPCommentDelete(TPCommentID): 
    TPDeleteComment = TPComment.objects.get(id=TPCommentID)
    TPDeleteComment.delete()
    flash('The comments was deleted.')
    return redirect(url_for('therapist',therapistID=TPDeleteComment.therapist.id)) 
