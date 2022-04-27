from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Post, Comment
from app.classes.forms import PostForm, CommentForm
from flask_login import login_required
import datetime as dt

@app.route('/post/list')
@login_required
def postList():
    posts = Post.objects()
    return render_template('posts.html',posts=posts)

@app.route('/post/<postID>')

@login_required
def post(postID):

    thisPost = Post.objects.get(id=postID)

    theseComments = Comment.objects(post=thisPost)

    return render_template('post.html',post=thisPost,comments=theseComments)


@app.route('/post/delete/<postID>')

@login_required
def postDelete(postID):

    deletePost = Post.objects.get(id=postID)

    if current_user == deletePost.author:
 
        deletePost.delete()

        flash('The Post was deleted.')
    else:
        
        flash("You can't delete a post you don't own.")

    posts = Post.objects()  

    return render_template('posts.html',posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])

@login_required

def postNew():

    form = PostForm()

    if form.validate_on_submit():

  
        newPost = Post(
            
            subject = form.subject.data,
            content = form.content.data,
            posttopic = form.posttopic.data,
            author = current_user.id,
            
            modifydate = dt.datetime.utcnow
        )
        
        newPost.save()

        return redirect(url_for('post',postID=newPost.id))

    return render_template('postform.html',form=form)

@app.route('/post/edit/<postID>', methods=['GET', 'POST'])
@login_required
def postEdit(postID):
    editPost = Post.objects.get(id=postID)
    
    if current_user != editPost.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('post',postID=postID))
    
    form = PostForm()
    
    if form.validate_on_submit():
        
        editPost.update(
            subject = form.subject.data,
            content = form.content.data,
            posttopic = form.posttopic.data,
            modifydate = dt.datetime.utcnow
        )
        
        return redirect(url_for('post',postID=postID))

    form.subject.data = editPost.subject
    form.content.data = editPost.content
    form.posttopic.data = editPost.posttopic

    return render_template('postform.html',form=form)

@app.route('/comment/new/<postID>', methods=['GET', 'POST'])
@login_required
def commentNew(postID):
    post = Post.objects.get(id=postID)
    form = CommentForm()
    if form.validate_on_submit():
        newComment = Comment(
            author = current_user.id,
            post = postID,
            content = form.content.data
        )
        newComment.save()
        return redirect(url_for('post',postID=postID))
    return render_template('commentform.html',form=form,post=post)

@app.route('/comment/edit/<commentID>', methods=['GET', 'POST'])
@login_required
def commentEdit(commentID):
    editComment = Comment.objects.get(id=commentID)
    if current_user != editComment.author:
        flash("You can't edit a comment you didn't write.")
        return redirect(url_for('post',postID=editComment.post.id))
    post = Post.objects.get(id=editComment.post.id)
    form = CommentForm()
    if form.validate_on_submit():
        editComment.update(
            content = form.content.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('post',postID=editComment.post.id))

    form.content.data = editComment.content

    return render_template('commentform.html',form=form,post=post)   

@app.route('/comment/delete/<commentID>')
@login_required
def commentDelete(commentID): 
    deleteComment = Comment.objects.get(id=commentID)
    deleteComment.delete()
    flash('The comments was deleted.')
    return redirect(url_for('post',postID=deleteComment.post.id)) 
