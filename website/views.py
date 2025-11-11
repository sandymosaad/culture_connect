# Import necessary packages from Flask
from flask import Blueprint, render_template, session, flash, redirect, url_for, request, current_app
import datetime  # For handling dates
import os        # For working with files and directories
from .shared import add_item, get_items,update_posts
# Define a Blueprint to organize routes
views = Blueprint('views', __name__)

# Define the Post class to store information for each post
class Post:
    def __init__(self, title, body, country, category, date, flag, username, id, post_image=None):
        # Basic attributes of the post
        self.title = title
        self.body = body
        self.country = country
        self.category = category
        self.date = date
        self.flag = flag
        self.username = username
        self.id = id
        self.post_image = post_image  # Optional post image

    # Method to convert the Post object to a dictionary
    def to_dict(self):
        return {
            "title": self.title,
            "body": self.body,
            "country": self.country,
            "category": self.category,
            "date": str(self.date),
            "flag": self.flag,
            "username": self.username,
            "post_id" : self.id,
            "post_image": self.post_image,

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
                id =None,
                post_image= new_name_post_image
                )
        else:
            # Create a new Post object without a post image
            new_post = Post(
                post_data['title'],
                post_data['body'],
                post_data['country'],
                post_data['category'],
                post_data['date'],
                new_name_flag,
                username,
                id =None,
                )
        
        # Convert the post to a dictionary to pass to the template
        post_dict = new_post.to_dict()
            
        add_item(post_dict, 'posts')
        user_posts = get_user_posts(username)

        #return render_template('profile.html', custom_style="profile", username = username ,posts = user_posts)
        return redirect(url_for('views.profile'))
    
    user_posts = get_user_posts(username)
    # Render the profile page for GET requests
    return render_template('profile.html', custom_style="profile", username = username ,posts = user_posts)


# get all posts for the current user
def get_user_posts(username):
    all_posts =get_items('posts')
    user_posts = []
    for post in all_posts['posts']:
        if (post["username"] == username):
            user_posts.append(post)
    return user_posts


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
        date = str(datetime.date.today())  # Today's date string to can story it in json
        return {
        "title": title,
        "body": body,
        "country": country,
        "category": category,
        "date": date,
        "flag_file": flag_file,
        "post_image_file": post_image_file
        }



@views.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    try:
        posts = get_items('posts')
        posts = [p for p in posts['posts'] if int(p["post_id"]) != int(post_id)]
        update_posts('posts',posts)
        return {"success": True}
    except Exception as e:
        print("DELETE ERROR:", e)
        return {"success": False, "error": str(e)}, 500 