import pymysql
from flask import Flask
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = generate_password_hash('daniel-shelby', method='pbkdf2')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://admin:admin@localhost/dotacamp"
    app.static_folder = 'static'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .post import post as post_blueprint
    app.register_blueprint(post_blueprint)

    from .navi import navi as navi_blueprint
    app.register_blueprint(navi_blueprint)

    with app.app_context():
        db.create_all()
    return app

