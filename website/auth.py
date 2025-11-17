from flask import Blueprint, render_template, redirect, url_for, request , flash, session
from os import path
import json
from .shared import add_item, get_items, save_image
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
    
        data = get_items('users')
        users =data['users']
        #users = get_items('users')
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
        username_input = request.form.get('username')
        email_input= request.form.get('email')
        password_input = request.form.get('password')
        profile_file = request.files.get('profile')  
        response = valid_sign_up_data(username_input, email_input, password_input)
        if response:
            return response

        users_data = get_usernames_and_emails()
        if username_input in users_data['usernames']:
            flash(f'Username "{username_input}" already exists', category='error')
            return render_template("signup.html", custom_style='auth', username= username_input, email=email_input,password=password_input, has_diff_navbar_style=True, errors={}) 
        
        if email_input in users_data['emails']:
            flash('Email already exists', category='error')
            return render_template("signup.html", custom_style='auth', username= username_input, email=email_input,password=password_input, has_diff_navbar_style=True, errors={}) 
        
        new_name_profile =save_image(profile_file, 'profile',username_input )
        new_user = {
            "username": username_input,
            "email": email_input,
            "password": password_input,
            'profile_img': new_name_profile
        }
        
        add_item(new_user,'users')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', custom_style='auth', has_diff_navbar_style=True,  errors={})

def valid_sign_up_data(username, email, password):
    pattern_username = r'^[a-zA-Z]{3,}[a-zA-Z0-9_]*$'
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

def get_usernames_and_emails():
    data = get_items('users')
    users = data.get('users', [])

    usernames = [user['username'] for user in users]
    emails = [user['email'] for user in users]

    return {
        "usernames": usernames,
        "emails": emails
    }
    