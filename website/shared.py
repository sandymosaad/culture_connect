from os import path
import json
from flask import  current_app

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
    data = None
    # If file doesn't exist yet,or empty start with empty list
    #------------------
    if not path.exists(file_path) or path.getsize(file_path) == 0:
        data = {
            "next_id": 1,
            file_name: []  
        }
    else:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except:
            data = {
                "next_id": 1,
                file_name: []
            }
    new_id = data['next_id']
    item['id'] = new_id
    
    data[file_name].append(item)
    data['next_id'] = new_id + 1
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

        
        
#######################
# get items 
#######################
def get_items(file_name): 
    file_path = get_db_path(file_name)
    if not path.exists(file_path) or path.getsize(file_path) == 0:
            return {
                "next_id": 1,
                file_name: []
            }
        
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        # Handle corrupted file case
        return {
            "next_id": 1,
            file_name: []
            }


######################################
#  Function to save uploaded images and return the new filename
######################################
def save_image(file, type_image, username, id):
    # Extract the file extension
    ext = file.filename.rsplit('.', 1)[1]
    # Create a new filename like "username_type.ext"
    new_name = f"{username}_{type_image}_{id}.{ext}"
    # Full path where the file will be saved
    save_path = path.join(current_app.config['UPLOAD_FOLDER'], new_name)
    # Save the file to the server
    file.save(save_path)
    return new_name