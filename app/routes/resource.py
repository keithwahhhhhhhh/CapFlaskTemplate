from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Resource, resComment
from app.classes.forms import ResourceForm, resCommentForm
from flask_login import login_required
import datetime as dt


@app.route('/resource/list')

@login_required
def resourceList():

    resources = Resource.objects()

    return render_template('resources.html',resources=resources)


@app.route('/resource/<resourceID>')

@login_required
def resource(resourceID):
  
    thisResource = Resource.objects.get(id=resourceID)
   
    resTheseComments = resComment.objects(resource=thisResource)

    return render_template('resource.html',resource=thisResource, resComments = resTheseComments)


@app.route('/resource/delete/<resourceID>')

@login_required
def resourceDelete(resourceID):

    deleteResource = Resource.objects.get(id=resourceID)

    if current_user == deleteResource.author:

        deleteResource.delete()

        flash('The Resource was deleted.')
    else:

        flash("You can't delete a resource you don't own.")

    resources = Resource.objects()  

    return render_template('resources.html',resources=resources)


@app.route('/resource/new', methods=['GET', 'POST'])

@login_required

def resourceNew():

    form = ResourceForm()

    if form.validate_on_submit():


        newResource = Resource(

            topic = form.topic.data,
            description = form.description.data,
            restype = form.restype.data,
            link = form.link.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )

        newResource.save()


        return redirect(url_for('resource',resourceID=newResource.id))


    return render_template('resourceform.html',form=form)



@app.route('/resource/edit/<resourceID>', methods=['GET', 'POST'])
@login_required
def ResourceEdit(resourceID):
    editResource = Resource.objects.get(id=resourceID)

    if current_user != editResource.author:
        flash("You can't edit a resource you don't own.")
        return redirect(url_for('resource',resourceID=resourceID))

    form = ResourceForm()

    if form.validate_on_submit():

        editResource.update(
            topic = form.topic.data,
            description = form.description.data,
            link = form.link.data,
            restype = form.restype.data,
            modifydate = dt.datetime.utcnow
        )

        return redirect(url_for('resource',resourceID=resourceID))


    form.topic.data = editResource.topic
    form.description.data = editResource.description
    form.restype.data = editResource.restype
    form.link.data = editResource.link


    return render_template('resourceform.html',form=form)



@app.route('/resComment/new/<resourceID>', methods=['GET', 'POST'])
@login_required
def resCommentNew(resourceID):
    resource = Resource.objects.get(id=resourceID)
    form = resCommentForm()
    if form.validate_on_submit():
        newResComment = resComment(
            author = current_user.id,
            resource = resourceID,
            resDescription = form.resDescription.data
            
        )
        newResComment.save()
        return redirect(url_for('resource',resourceID=resourceID))
    return render_template('resourcescommentform.html',form=form,resource=resource)

@app.route('/comment/edit/<commentID>', methods=['GET', 'POST'])
@login_required
def resCommentEdit(resCommentID):
    resEditComment = resComment.objects.get(id=resCommentID)
    if current_user != resEditComment.author:
        flash("You can't edit a comment you didn't write.")
        return redirect(url_for('resource',resourceID=resEditComment.resource.id))
    resource = Resource.objects.get(id=resEditComment.resource.id)
    form = resCommentForm()
    if form.validate_on_submit():
        resEditComment.update(
            resDescription = form.resDescription.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('resource',resourceID=resEditComment.resource.id))

    form.resDescription.data = resEditComment.resDescription

    return render_template('resourcesCommentForm.html',form=form,resource=resource)   

@app.route('/comment/delete/<commentID>')
@login_required
def resCommentDelete(resCommentID): 
    resDeleteComment = resComment.objects.get(id=resCommentID)
    resDeleteComment.delete()
    flash('The comments was deleted.')
    return redirect(url_for('resource',resourceID=resDeleteComment.resource.id)) 
