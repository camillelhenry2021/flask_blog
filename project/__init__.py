import datetime
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Post
    # needed by Flask LoginManager()
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # create database
    if not Path('./instance/db.sqlite').exists():
        with app.app_context():
            db.create_all()
            # add admin user
            admin = User(
                email='admin@gmail.com', 
                name='admin', 
                password=generate_password_hash("admin", method='scrypt')
            )
            db.session.add(admin)
            db.session.commit()
            # add admin post
            admin_post = Post(
                user_id=admin.id,
                title="admin title",
                content="this is admin post",
                timestamp=datetime.datetime.now()
            )
            db.session.add(admin_post)
            db.session.commit()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app