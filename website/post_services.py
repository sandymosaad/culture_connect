from .shared import get_items, get_db_path, save_image
import datetime
import json

# -----------------------------------------
# Prepare post data from input fields
# -----------------------------------------
def prepare_post_data(title, body, category, post_image_file=None):
    """
    Prepares a post dictionary with title, body, category, date,
    and optionally uploaded files (post image).
    """
    date = datetime.date.today().strftime("%b %d, %Y")
    return {
        "title": title,
        "body": body,
        "category": category,
        "date": date,
        "post_image_file": post_image_file
    }


# -----------------------------------------
# Delete a post by its ID
# -----------------------------------------
def delete_post_by_id(id):
    """
    Deletes a post from the JSON database by post ID.
    Returns a tuple (success: bool, error_message: str or None)
    """
    try:
        posts = get_items('posts')
        posts = [p for p in posts['posts'] if int(p["id"]) != int(id)]
        update_posts('posts', posts)
        return True, None
    except Exception as e:
        return False, str(e)


# -----------------------------------------
# Edit a post by its ID
# -----------------------------------------
def edit_post_by_id(id, form_data, files,username):
    """
    Edits a post's details (title, body, category) and optionally updates images.
    Returns a tuple (success: bool, error_message: str or None)
    """
    try:
        data = get_items("posts")
        posts = data["posts"]
        for post in posts:
            if "id" in post and int(post["id"]) == int(id):
                post["title"] = form_data.get("title")
                post["body"] = form_data.get("body")
                post["category"] = form_data.get("category")

                # Update post image if provided
                if "post_image" in files and files["post_image"].filename:
                    img = files["post_image"]
                    post["post_image"] = save_image(img, 'post_image', username,id)

        update_posts("posts", posts)
        return True, None
    except Exception as e:
        return False, str(e)


# -----------------------------------------
# Update posts JSON file
# -----------------------------------------
def update_posts(file_name, posts):
    """
    Updates the JSON database with the given list of posts.
    """
    file_path = get_db_path(file_name)
    data = get_items(file_name)
    data[file_name] = posts
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
        

def get_countries_name(posts):
    """
    Returns a list of unique country names from posts.
    """
    countries_name=[]
    for post in posts:
        if post['user_country'] not in countries_name:
            countries_name.append(post['user_country'])
    return countries_name


