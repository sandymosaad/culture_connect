import re 
def valid_post_data(title, body):
    pattern_post_title = r'^(?=[\u0600-\u06FFa-zA-Z0-9\s\-\_,\/\.]*[\u0600-\u06FFa-zA-Z]{3,})[\u0600-\u06FFa-zA-Z][\u0600-\u06FFa-zA-Z0-9\s\-\_,\/\.]*$'
    pattern_post_body = r'^(?=(?:.*[a-zA-Z\u0600-\u06FF]){10,}).{30,}$'

    errors = {}

    if not re.match(pattern_post_title, title):
        errors['title_error'] = "Title must start with a letter and contain at least 3 letters. Numbers, spaces, and symbols - _ , / . are allowed."

    if not re.match(pattern_post_body, body):
        errors['body_error'] = "Body must be at least 30 characters long and contain at least 10 letters (Arabic or English)."

    return errors


def valid_sign_up_data(username, email, password, country):
    pattern_username = r'^[a-zA-Z][a-zA-Z0-9_]{2,19}$'
    pattern_email = r'^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.(com|net|org|io|edu)$'
    pattern_password = r'^[a-zA-Z0-9_\- @#]{8,}$'
    pattern_user_country = r'^[A-Za-z]+(?:[ \-][A-Za-z]+)*$'

    errors ={}

    if not re.match(pattern_username, username):
        errors["username_error"] = "Username must start with a letter and be 3-20 characters long, containing only letters, numbers, or _."


    if not re.match(pattern_email, email):
        errors["email_error"] = "Email must be valid, e.g., username@gmail.com (allowed domains: .com, .net, .org, .io, .edu)."

    if not re.match(pattern_password, password):
        errors["password_error"] = "Password must be at least 8 characters."
        
    if not re.match(pattern_user_country, country):
        errors["country_error"] = "Country name must contain only letters (English), spaces, or dash (-)."

    return errors 