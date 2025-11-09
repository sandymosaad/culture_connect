from flask import Blueprint, render_template,session, flash, redirect, url_for, request
import datetime 
views = Blueprint ('views', __name__)

@views.route('/')
def index():
    return render_template('index.html', custom_style="index")

@views.route('/profile', methods=['POST', 'GET'])
def profile():
    username = session.get('username')
    if not username:
        flash('Please log in first', category='error')
        return redirect(url_for('auth.login'))
    if request.method=='POST':
        title = request.form.get('title')
        body = request.form.get('body')
        country = request.form.get('country')
        category = request.form.get('category')
        date = datetime.date.today()
        
    
    return render_template('profile.html', custom_style="profile", username = username,category=category,country=country,title=title,body=body,date=date   )


# @views.route('/add-post', methods=['POST'])
# def add_post():
#     return "Received"
