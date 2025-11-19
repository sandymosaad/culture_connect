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

    data = get_items('users')
    users = data.get('users', [])


    for u in users:
        if  u['username'] == username:
            user_id = u['id']
            user_profile_img = u['user_profile_img']
            user_country = u['user_country']
            user_flag_country_img = u['user_flag_country_img']
            
    if request.method == 'POST':
        
        post_data = prepare_post_data(
            title=request.form.get('title'),
            body=request.form.get('body'),
            category=request.form.get('category'),
            post_image_file=request.files.get('post_image')
        )
        errors = valid_post_data(post_data['title'], post_data['body'])

        if errors:
            show_modal = True  
        else:
            id = get_items("posts")['next_id']   
            # Save post image if exists
            post_image_name = save_image(post_data['post_image_file'], 'post_image', username,id ) if post_data['post_image_file'] else None

                    
            new_post = Post(
                title=post_data['title'],
                body=post_data['body'],
                category=post_data['category'],
                date=post_data['date'],
                id = id,
                user_id=user_id,
                post_image=post_image_name,
                
            )
            print(user_id)
            add_item(new_post.to_dict(), 'posts')
            return redirect(url_for('views.profile'))
            
    user_posts = Post.get_user_posts(user_id)[::-1]
    
    for post in user_posts:
        post['username'] = username
        post['user_profile_img'] = user_profile_img
        post['user_country'] =  user_country
        post['user_flag_country_img'] =user_flag_country_img


    return render_template('profile.html',
                        custom_style="profile",
                        username=username,
                        posts=user_posts,
                        errors=errors,
                        show_modal=show_modal,
                        form_data=request.form if errors else {}
    )

@views.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    success, error = delete_post_by_id(id)
    if success:
        return {"success": True}
    return {"success": False, "error": error}, 500


@views.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    username = session.get('username')
    form_data = request.form
    files = request.files
    success, error = edit_post_by_id(id, form_data, files,username)
    if success:
        return {"success": True}
    return {"success": False, "error": error}, 500

@views.route('/global')
def global_posts():
    username = session.get('username')
    posts_data = get_items("posts")   
    all_posts = posts_data["posts"][::-1]
    users_data = get_items("users")   
    all_users = {user['id']: user for user in users_data["users"]}
    
    for post in all_posts:
        user = all_users.get(post['user_id'])
        if user:
            post['username'] = user['username']
            post['user_profile_img'] = user['user_profile_img']
            post['user_country'] = user['user_country']
            post['user_flag_country_img'] = user['user_flag_country_img']
    
    countries_name= get_countries_name(all_posts)

    return render_template('global_posts.html', custom_style="global", posts=all_posts,  countries_name = countries_name,username=username)

