from flask import Blueprint, render_template, redirect, url_for, request , flash, session
from .models import User
from .shared import add_item, get_items, save_image
from .validators import valid_sign_up_data
auth = Blueprint('auth', __name__)

#######################
# login 
#######################

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
    
        data = get_items('users')
        users =data['users']
        
        user_found = None
        for user in users:
            if user['email'] == email:
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
        profile_file_input = request.files.get('profile')
        flag_file_input = request.files.get('flag')
        country_input = request.form.get('country')

        errors = valid_sign_up_data(username_input, email_input, password_input, country_input)

        if errors:
            return render_template("signup.html", custom_style='auth',
                                username =username_input, email = email_input,
                                password =  password_input, country = country_input,
                                has_diff_navbar_style = True, errors = errors) 

        users_data = extract_usernames_and_emails()
        if username_input in users_data['usernames']:
            flash(f'Username "{username_input}" already exists', category='error')
            return render_template("signup.html", custom_style='auth', username= username_input, email=email_input,password=password_input, has_diff_navbar_style=True, errors={}) 
        
        if email_input in users_data['emails']:
            flash('Email already exists', category='error')
            return render_template("signup.html", custom_style='auth', username= username_input, email=email_input,password=password_input, has_diff_navbar_style=True, errors={}) 
        
        id = get_items("users")['next_id']   
        new_name_profile =save_image(profile_file_input, 'profile', username_input,id )
        new_name_flag =save_image(flag_file_input, 'flag', username_input,id)

        # Create user object
        new_user = User(
            id=None,
            username=username_input,
            email=email_input,
            password=password_input,
            user_profile_img=new_name_profile,
            user_country=country_input,
            user_flag_country_img=new_name_flag
        )
                # Save to JSON
        add_item(new_user.to_dict(), "users")
        return redirect(url_for('auth.login'))

    return render_template('signup.html', custom_style='auth', has_diff_navbar_style=True,  errors={})


def extract_usernames_and_emails():
    data = get_items('users')
    users = data.get('users', [])

    usernames = [user['username'] for user in users]
    emails = [user['email'] for user in users]

    return {
        "usernames": usernames,
        "emails": emails
    }
    