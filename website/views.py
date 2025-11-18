# Import necessary packages from Flask
from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from .shared import add_item, get_items, save_image
from .models import Post 
from .validators import valid_post_data
from .post_services import  prepare_post_data, delete_post_by_id, edit_post_by_id, get_countries_name

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
        
        post_data = prepare_post_data(
            title=request.form.get('title'),
            body=request.form.get('body'),
            category=request.form.get('category'),
            post_image_file=request.files.get('post-img')
        )
        errors = valid_post_data(post_data['title'], post_data['body'])

        if errors:
            show_modal = True  
        else:
            id = get_items("posts")['next_id']   
            # Save post image if exists
            post_image_name = save_image(post_data['post_image_file'], 'post_image', username,id ) if post_data['post_image_file'] else None

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
    
    user_posts = Post.get_user_posts(username)[::-1]
    return render_template('profile.html', custom_style="profile", username=username, posts=user_posts, errors=errors, show_modal=show_modal, form_data=request.form if errors else {}
    )

@views.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    success, error = delete_post_by_id(id)
    if success:
        return {"success": True}
    return {"success": False, "error": error}, 500


@views.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    form_data = request.form
    files = request.files
    success, error = edit_post_by_id(id, form_data, files)
    if success:
        return {"success": True}
    return {"success": False, "error": error}, 500

@views.route('/global')
def global_posts():
    username = session.get('username')
    data = get_items("posts")   
    all_posts = data["posts"][::-1]
    countries_name= get_countries_name(all_posts)

    return render_template('global_posts.html', custom_style="global", posts=all_posts, countries_name = countries_name , username = username)

