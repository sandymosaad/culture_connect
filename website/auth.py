from flask import Blueprint, render_template, redirect, url_for, request , flash, session
from os import path
import json
from .shared import add_item, get_items
import re
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

    return render_template('login.html', custom_style='auth', has_diff_navbar_style=True)

#######################
# logout
#######################
@auth.route('/logout')
def logout():
    username = session.get('username')
    if(username):
        session.pop('username')
        flash('Logged out successfully!', category='success')
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
        response = valid_sign_up_data(username, email, password)
        if response:
            return response

        # if len(get_items('users')) == 0:
        #     id=1
        # else:
        #     id=len(get_items('users')) + 1
        new_user = {
            
            "username": username,
            "email": email,
            "password": password
        }
        add_item(new_user,'users')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', custom_style='auth', has_diff_navbar_style=True,  errors={})

def valid_sign_up_data(username, email, password):
    pattern_username = r'^[a-zA-Z]{3,}[_\0-9]*[a-zA-Z0-9]?$'
    pattern_email =r'^[a-zA-Z]+[a-zA-Z0-9_-]*@(gmail|yahoo|outlook)\.com$'
    pattern_password = r'^[a-zA-Z0-9_\- @#]{8,}$'
    errors ={}
   
    if not re.match(pattern_username, username):
        errors["username_error"] = "Username must be at least 3 characters and contain only letters, numbers or _ ."

    if not re.match(pattern_email, email):
        errors["email_error"] = "Email must be valid, e.g., username@gmail.com."

    if not re.match(pattern_password, password):
        errors["password_error"] = "Password must be at least 8 characters."

    if errors:
        return render_template("signup.html", custom_style='auth', username=username, email=email,password=password, has_diff_navbar_style=True, errors=errors) 
    
    return None