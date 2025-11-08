from flask import Blueprint, render_template, redirect, url_for, request 
from os import path
import json
auth = Blueprint('auth', __name__)


#######################
# get path
#######################
def get_db_path(filename):
    """
    Returns the absolute path to a JSON database file inside the 'db' folder.
    """
    base_dir = path.dirname(path.abspath(__file__))      # website/
    project_root = path.dirname(base_dir)                # project root
    db_path = path.join(project_root, "db", f"{filename}.json")
    return db_path

#######################
# add user 
#######################
def add_user(user):
    """
    Adds a new user object to users.json.
    user must be a dictionary: {"id": 1, "username": "...", "email": "...", "password": "..."}
    """
    file_path = get_db_path('users')

    # If file doesn't exist yet, start with empty list
    if not path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

    if path.getsize(file_path) == 0:
        users = []
    else:
        with open(file_path, 'r') as f:
            users = json.load(f)

    # Add new user
    users.append(user)

    # Write updated list back
    with open(file_path, 'w') as f:
        json.dump(users, f, indent=4)
        
#######################
# get users 
#######################
def get_users():
    file_path = get_db_path('users')
    if not path.exists(file_path):
        return []
    if path.getsize(file_path) == 0:
        return []
    with open(file_path, 'r') as f:
        users = json.load(f)
        return users

    
#######################
# login 
#######################
@auth.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html', custom_style='auth')

#######################
# logout
#######################
@auth.route('/logout')
def logout():
    return redirect(url_for('/auth.login'))

#######################
# sign up
#######################
@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if len(get_users()) == 0:
            id=1
        else:
            id=len(get_users()) + 1
        new_user = {
            "id": id,
            "username": username,
            "email": email,
            "password": password
        }
        add_user(new_user)
        return redirect(url_for('auth.login'))

    return render_template('signup.html', custom_style='auth')
