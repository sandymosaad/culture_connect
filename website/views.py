from flask import Blueprint, render_template,session, flash, redirect, url_for, request, current_app
import datetime 
import os

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
    post =None
    if request.method=='POST':
        title = request.form.get('title')
        body = request.form.get('body')
        country = request.form.get('country')
        category = request.form.get('category')
        flag_file = request.files.get('flag')
        post_image_file = request.files.get('post_image')
        date = datetime.date.today()    
        
        new_name_flag = save_image(flag_file ,'flag' ,username)
        new_name_post_image = save_image( post_image_file, 'post_image' , username)

        post = {
            "title": title,
            "body": body,
            "country": country,
            "category": category,
            "date": date,
            "flag": new_name_flag,
            "post_image": new_name_post_image,
            "username": username
        }
        return render_template('profile.html', username = username, post=post ,  custom_style="profile" )
    
    return render_template('profile.html', custom_style="profile" )

# save the image and return the new name
def save_image(file, type_image ,username ):
        ext =file.filename.rsplit('.', 1)[1]
        new_name = f"{username}_{type_image}.{ext}"

        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_name)
        file.save(save_path)
        return new_name
    
# def get_data():
#     if request.method=='POST':
#         title = request.form.get('title')
#         body = request.form.get('body')
#         country = request.form.get('country')
#         category = request.form.get('category')
#         date = datetime.date.today()
#         return [title, body, country, category, date]
# @views.route('/add-post', methods=['POST'])
# def add_post():
#     return "Received"
