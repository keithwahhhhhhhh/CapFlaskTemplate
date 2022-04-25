from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/activities')
def activities():
    return render_template('activities.html')
