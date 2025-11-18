from .shared import  get_items

# Define the Post class to store information for each post
class Post:
    def __init__(self, title, body, category, date,id, user_id, post_image=None):
        # Basic attributes of the post
        self.title = title
        self.body = body
        self.category = category
        self.date = date
        self.id = id
        self.user_id =user_id
        self.post_image = post_image  # Optional post image

    # Method to convert the Post object to a dictionary
    def to_dict(self):
        return {
            "title": self.title,
            "body": self.body,
            "category": self.category,
            "date": str(self.date),
            "id" : self.id,
            "user_id": self.user_id,
            "post_image": self.post_image,
        }


    @classmethod
    def get_user_posts(cls, user_id):
        """
        Return a list of Post objects for the given username.
        """
        data = get_items("posts")
        all_posts = data["posts"]
        user_posts = [post for post in all_posts if post["user_id"] == user_id]

        return user_posts


# Define the User class to store information for each user

class User:
    def __init__(self, id, username, email, password, user_profile_img, user_country, user_flag_country_img):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.user_profile_img = user_profile_img
        self.user_country = user_country
        self.user_flag_country_img = user_flag_country_img
    
    # Method to convert the User object to a dictionary
    def to_dict(self):
        return {
            "id" : self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            'user_profile_img':self.user_profile_img,
            'user_country' : self.user_country,
            'user_flag_country_img' : self.user_flag_country_img,
        }