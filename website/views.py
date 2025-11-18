# Import necessary packages from Flask
from flask import Blueprint, render_template, session, flash, redirect, url_for, request, current_app
import datetime  # For handling dates  
import os        # For working with files and directories
from .shared import add_item, get_items, update_posts,save_image
from .models import Post
import re 

# Define a Blueprint to organize routes
views = Blueprint('views', __name__)

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

    errors = {}
    show_modal = False  

    if request.method == 'POST':
        
        post_data = get_post_data()
        errors = valid_post_data(post_data['title'], post_data['body'])

        if errors:
            show_modal = True  
        else:

            # Save post image if exists
            post_image_name = save_image(post_data['post_image_file'], 'post_image', username) if post_data['post_image_file'] else None

            data = get_items('users')
            users = data.get('users', [])
            for u in users:
                if  u['username'] == username:
                    user_profile_img = u['user_profile_img']
                    user_country = u['user_country']
                    user_flag_country_img = u['user_flag_country_img']
                    
                    
            
            new_post = Post(
                title=post_data['title'],
                body=post_data['body'],
                category=post_data['category'],
                date=post_data['date'],
                username=username,
                id = None,
                user_profile_img=user_profile_img,
                user_country = user_country,
                user_flag_country_img = user_flag_country_img,
                post_image=post_image_name,
                
            )
            add_item(new_post.to_dict(), 'posts')
            return redirect(url_for('views.profile'))
    user_posts = get_user_posts(username)[::-1]
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
    all_posts = data["posts"][::-1]
    countries_name= get_countries_name(all_posts)

    return render_template('global_posts.html', custom_style="global", posts=all_posts, countries_name = countries_name , username = username)

def get_countries_name(posts):
    countries_name=[]
    for post in posts:
        if post['user_country'] not in countries_name:
            countries_name.append(post['user_country'])
    return countries_name


def valid_post_data(title, body):
    pattern_post_title = r'^[\u0600-\u06FFa-zA-Z0-9][\u0600-\u06FFa-zA-Z0-9\s\-\_,\.]{2,}$'
    pattern_post_body = r'^.{30,}$'
    pattern_post_country = r'^[\u0600-\u06FFa-zA-Z\s]{3,}$'

    errors = {}

    if not re.match(pattern_post_title, title):
        errors['title_error'] = "Title must be at least 3 characters and can include Arabic/English letters, numbers, spaces, and basic symbols."

    if not re.match(pattern_post_body, body):
        errors['body_error'] = "Body must be at least 30 characters."


    return errors