from os import path
import json

def get_db_path(filename):
    """
    Returns the absolute path to a JSON database file inside the 'db' folder.
    """
    base_dir = path.dirname(path.abspath(__file__))      # website/
    project_root = path.dirname(base_dir)                # project root
    db_path = path.join(project_root, "db", f"{filename}.json")
    return db_path

#######################
# add item 
#######################
def add_item(item ,file_name ):
    """
    Adds a new user object to file_name.json.
    user must be a dictionary: {"id": 1, "username": "...", "email": "...", "password": "..."}
    """
    file_path = get_db_path(file_name)

    # If file doesn't exist yet, start with empty list
    if not path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

    if path.getsize(file_path) == 0:
        items = []
    else:
        with open(file_path, 'r') as f:
            items = json.load(f)

    # Add new item
    items.append(item)

    # Write updated list back
    with open(file_path, 'w') as f:
        json.dump(items, f, indent=4)
        
        
#######################
# get items 
#######################
def get_items(file_name): 
    file_path = get_db_path(file_name)
    if not path.exists(file_path):
        return []
    if path.getsize(file_path) == 0:
        return []
    with open(file_path, 'r') as f:
        items = json.load(f)
        return items


def update_posts(file_name , posts):
    file_path = get_db_path(file_name)
    with open(file_path, 'w') as f:
        json.dump(posts, f, indent=4)
