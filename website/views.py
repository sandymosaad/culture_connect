# Import necessary packages from Flask
from flask import Blueprint, render_template, session, flash, redirect, url_for, request, current_app
import datetime  # For handling dates
import os        # For working with files and directories

# Define a Blueprint to organize routes
views = Blueprint('views', __name__)

# Define the Post class to store information for each post
class Post:
    def __init__(self, title, body, country, category, date, flag, username, post_image=None):
        # Basic attributes of the post
        self.title = title
        self.body = body
        self.country = country
        self.category = category
        self.date = date
        self.flag = flag
        self.post_image = post_image  # Optional post image
        self.username = username

    # Method to convert the Post object to a dictionary
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

# Homepage route
@views.route('/')
def index():
    return render_template('index.html', custom_style="index")

# Profile page route
@views.route('/profile', methods=['POST', 'GET'])
def profile():
    # Get the username from the session
    username = session.get('username')
    
    # If the user is not logged in, redirect to login
    if not username:
        flash('Please log in first', category='error')
        return redirect(url_for('auth.login'))
    
    # Handle POST request when creating a new post
    if request.method == 'POST':
        # Get form data
        post_data = get_post_data()

        # Save the flag image and get the new filename
        new_name_flag = save_image(post_data['flag_file'], 'flag', username)
        
        # Save post image if provided
        if post_data['post_image_file']:
            new_name_post_image = save_image(post_data['post_image_file'], 'post_image', username)
            # Create a new Post object with the post image
            new_post = Post(
                post_data['title'],
                post_data['body'],
                post_data['country'],
                post_data['category'],
                post_data['date'],
                new_name_flag,
                username,
                new_name_post_image)
        else:
            # Create a new Post object without a post image
            new_post = Post(
                post_data['title'],
                post_data['body'],
                post_data['country'],
                post_data['category'],
                post_data['date'],
                new_name_flag,
                username)
        
        # Convert the post to a dictionary to pass to the template
        post_dict = new_post.to_dict()
        
        # Render the profile page with the new post
        return render_template('profile.html', username=username, post=post_dict, custom_style="profile")
    
    # Render the profile page for GET requests
    return render_template('profile.html', custom_style="profile")

# Function to save uploaded images and return the new filename
def save_image(file, type_image, username):
    # Extract the file extension
    ext = file.filename.rsplit('.', 1)[1]
    # Create a new filename like "username_type.ext"
    new_name = f"{username}_{type_image}.{ext}"
    # Full path where the file will be saved
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_name)
    # Save the file to the server
    file.save(save_path)
    return new_name

# Get form data
def get_post_data():
        title = request.form.get('title')
        body = request.form.get('body')
        country = request.form.get('country')
        category = request.form.get('category')
        flag_file = request.files.get('flag')            # Country flag
        post_image_file = request.files.get('post_image')  # Optional post image
        date = datetime.date.today()  # Today's date
        return {
        "title": title,
        "body": body,
        "country": country,
        "category": category,
        "date": date,
        "flag_file": flag_file,
        "post_image_file": post_image_file
        }

