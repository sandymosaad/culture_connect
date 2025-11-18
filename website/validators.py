import re 
def valid_post_data(title, body):
    pattern_post_title = r'^[\u0600-\u06FFa-zA-Z0-9][\u0600-\u06FFa-zA-Z0-9\s\-\_,\/\.]{2,}$'
    pattern_post_body = r'^.{30,}$'

    errors = {}

    if not re.match(pattern_post_title, title):
        errors['title_error'] = "Title must be at least 3 characters and can include Arabic/English letters, numbers, spaces, and basic symbols."

    if not re.match(pattern_post_body, body):
        errors['body_error'] = "Body must be at least 30 characters."

    return errors


def valid_sign_up_data(username, email, password, country):
    pattern_username = r'^[a-zA-Z]{3,}[a-zA-Z0-9_]*$'
    pattern_email =r'^[a-zA-Z]+[a-zA-Z0-9_-]*@(gmail|yahoo|outlook)\.com$'
    pattern_password = r'^[a-zA-Z0-9_\- @#]{8,}$'
    pattern_user_country = r'^[\u0600-\u06FFa-zA-Z\s]{3,}$'

    errors ={}

    if not re.match(pattern_username, username):
        errors["username_error"] = "Username must be at least 3 characters and contain only letters, numbers or _ ."

    if not re.match(pattern_email, email):
        errors["email_error"] = "Email must be valid, e.g., username@gmail.com."

    if not re.match(pattern_password, password):
        errors["password_error"] = "Password must be at least 8 characters."
        
    if not re.match(pattern_user_country, country):
        errors["country_error"] = "Invalid country name."

    return errors 