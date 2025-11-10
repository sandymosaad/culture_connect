from flask import Blueprint, render_template,session, flash, redirect, url_for, request, current_app
import datetime 
import os

views = Blueprint ('views', __name__)

class Post:
    def __init__(self, title, body, country, category, date, flag, username,post_image=None):
        self.title = title
        self.body = body
        self.country = country
        self.category = category
        self.date = date
        self.flag = flag
        self.post_image = post_image
        self.username = username

    def to_dict(self):
        return {
            "title": self.title,
            "body": self.body,
            "country": self.country,
            "category": self.category,
            "date": self.date,
            "flag": self.flag,
            "post_image": self.post_image,
            "username": self.username
        }
      

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
        flag_file = request.files.get('flag')
        post_image_file = request.files.get('post_image')
        date = datetime.date.today()    
        
        new_name_flag = save_image(flag_file ,'flag' ,username)
        if post_image_file:
            new_name_post_image = save_image( post_image_file, 'post_image' , username)
            new_post =Post(title, body, country, category, date, new_name_flag, username , new_name_post_image)
        else:
            new_post =Post(title, body, country, category, date, new_name_flag, username )
        
        post_dict = new_post.to_dict()
        return render_template('profile.html', username = username, post=post_dict ,  custom_style="profile" )
    
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
