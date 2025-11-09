from flask import Blueprint, render_template,session, flash, redirect, url_for

views = Blueprint ('views', __name__)

@views.route('/')
def index():
    return render_template('index.html', custom_style="index")

@views.route('/profile')
def profile():
    username = session.get('username')
    if not username:
        flash('Please log in first', category='error')
        return redirect(url_for('auth.login'))
    return render_template('profile.html', custom_style="profile", username = username)

@views.route('/add_post')
def add_post():
    return render_template('index.html', custom_style="index")
