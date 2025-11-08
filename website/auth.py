from flask import Blueprint, render_template, redirect, url_for, request 
from os import path

auth = Blueprint('auth', __name__)



def get_db_path(filename):
    """
    Returns the absolute path to a database text file inside the 'db' folder.
    """
    base_dir = path.dirname(path.abspath(__file__))  # current folder (website)
    project_root = path.dirname(base_dir)           # project root (culture_connect)
    db_path = path.join(project_root, "db", f"{filename}.txt")
    return db_path


def add_user(user):
    """
    Adds a new user record to the 'users.txt' database file.
    Each user is stored in the format: username-email-password
    """
    file_path = get_db_path('users')
    with open(file_path, 'a') as users_db:
        users_db.write(f'{user}\n')

#######################
# login 
#######################
@auth.route('/login')
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
        user_record = f'{username}-{email}-{password}'
        add_user(user_record)
        return redirect(url_for('auth.login'))

    return render_template('signup.html', custom_style='auth')
