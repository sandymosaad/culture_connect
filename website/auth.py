from flask import Blueprint, render_template, redirect, url_for, request , flash, session
from os import path
import json
from .shared import add_item, get_items
auth = Blueprint('auth', __name__)

#######################
# login 
#######################

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
        users = get_items('users')
        user_found = None
        for user in users:
            if user['username'] == username:
                user_found = user
                break

        if user_found:
            if password == user_found['password']:
                flash('Logged in successfully!', category='success')
                session['username']= user_found['username']
                return redirect(url_for('views.profile'  ))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash(f'User not found ', category='error')

    return render_template('login.html', custom_style='auth')

#######################
# logout
#######################
@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))

#######################
# sign up
#######################
@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if len(get_items('users')) == 0:
            id=1
        else:
            id=len(get_items('users')) + 1
        new_user = {
            "id": id,
            "username": username,
             "email": email,
            "password": password
        }
        add_item(new_user,'users')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', custom_style='auth')
