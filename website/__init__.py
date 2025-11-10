from flask import Flask
import os
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    from .views import views
    from .auth import auth

    app.config['UPLOAD_FOLDER'] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static',
        'uploads'
    )
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix ='/')
    
    return app
