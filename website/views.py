# Import necessary packages from Flask
from flask import Blueprint, render_template, session, flash, redirect, url_for, request, current_app
import datetime  # For handling dates  
import os        # For working with files and directories
from .shared import add_item, get_items,update_posts
import re 

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
            "id" : self.id,
            "post_image": self.post_image,

        }


# Homepage route
@views.route('/')
def index():
    # Get the username from the session
    username = session.get('username')
    return render_template("index.html", custom_style="index", has_diff_navbar_style=True , username = username)


# Profile page route
@views.route('/profile', methods=['POST', 'GET'])
def profile():
    username = session.get('username')
    if not username:
        flash('Please log in first', category='error')
        return redirect(url_for('auth.login'))

    user_posts = get_user_posts(username)
    errors = {}
    show_modal = False  

    if request.method == 'POST':
        
        post_data = get_post_data()
        errors = valid_post_data(post_data['title'], post_data['body'], post_data['country'])

        if errors:
            show_modal = True  
        else:
            # Save flag image
            new_name_flag = save_image(post_data['flag_file'], 'flag', username)

            # Save post image if exists
            post_image_name = save_image(post_data['post_image_file'], 'post_image', username) if post_data['post_image_file'] else None

            new_post = Post(
                title=post_data['title'],
                body=post_data['body'],
                country=post_data['country'],
                category=post_data['category'],
                date=post_data['date'],
                flag=new_name_flag,
                username=username,
                id = None,
                post_image=post_image_name
            )
            add_item(new_post.to_dict(), 'posts')
            return redirect(url_for('views.profile'))

    return render_template('profile.html', custom_style="profile", username=username, posts=user_posts, errors=errors, show_modal=show_modal, form_data=request.form if errors else {}
    )

# get all posts for the current user
def get_user_posts(username):
    data = get_items("posts")   
    all_posts = data["posts"]
    #all_posts =get_items('posts')
    user_posts = []
    for post in all_posts:
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
        post_image_file = request.files.get('post-img')  # Optional post image
        date = datetime.date.today().strftime("%b %d, %Y") # Today's date string to can story it in json
        
        return {
        "title": title,
        "body": body,
        "country": country,
        "category": category,
        "date": date,
        "flag_file": flag_file,
        "post_image_file": post_image_file
        }


@views.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    try:
        posts = get_items('posts')
        posts = [p for p in posts['posts'] if int(p["id"]) != int(id)]
        update_posts('posts',posts)
        return {"success": True}
    except Exception as e:
        print("DELETE ERROR:", e)
        return {"success": False, "error": str(e)}, 500 
    

@views.route('/edit/<int:id>', methods=['POST'])
def edit_post(id):
    data = get_items("posts")   
    posts = data["posts"]
    try:
        for post in posts:
            # if "id" not in post:
            #     print("POST WITHOUT ID:", post)
            if "id" in post and int(post["id"]) == int(id):
                post["title"] = request.form.get("title")
                post["body"] = request.form.get("body")
                post["country"] = request.form.get("country")
                post["category"] = request.form.get("category")
                
                if "post_image" in request.files and request.files["post_image"].filename:
                    post["post_image"] = save_image(request.files["post_image"], 'post_image', post['username'])
                
                if "flag" in request.files and request.files["flag"].filename:
                    post["flag"] = save_image(request.files["flag"], 'flag', post['username'])

                break
        update_posts("posts", posts)
        return {"success": True}
    except Exception as e:
        print("EDIT ERROR:", e)
        return {"success": False, "error": str(e)}, 500
    

@views.route('/global')
def global_posts():
    username = session.get('username')
    data = get_items("posts")   
    all_posts = data["posts"]
    countries_name= get_countries_name(all_posts)

    return render_template('global_posts.html', custom_style="global", posts=all_posts, countries_name = countries_name , username = username)

def get_countries_name(posts):
    countries_name=[]
    for post in posts:
        if post['country'] not in countries_name:
            countries_name.append(post['country'])
    return countries_name


def valid_post_data(title, body, country):
    pattern_post_title = r'^[\u0600-\u06FFa-zA-Z0-9][\u0600-\u06FFa-zA-Z0-9\s\-\_,\.]{2,}$'
    pattern_post_body = r'^.{30,}$'
    pattern_post_country = r'^[\u0600-\u06FFa-zA-Z\s]{3,}$'

    errors = {}

    if not re.match(pattern_post_title, title):
        errors['title_error'] = "Title must be at least 3 characters and can include Arabic/English letters, numbers, spaces, and basic symbols."

    if not re.match(pattern_post_body, body):
        errors['body_error'] = "Body must be at least 30 characters."

    if not re.match(pattern_post_country, country):
        errors['country_error'] = "Country name must be at least 3 letters and contain only Arabic/English letters and spaces."

    # if errors:
    #     return render_template('post_modal.html', custom_style="profile", username = username, posts = user_posts, title = title, body = body, country = country, has_diff_navbar_style = True, errors = errors)
    # return None
    return errors