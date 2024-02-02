import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import Users, Posts, Scores
from .funcs import get_max_id, allowed_extention, get_new_name_file
from . import db, create_app

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        flash("Выйдите из аккаунта для входа в другой.")
        return redirect(url_for('main.index'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')

    user = Users.query.filter_by(login=login).first()
    if not user:
        flash("Пользователя с логином [{}] не существует.".format(login))
        return redirect(url_for('auth.login'))
    if not check_password_hash(user.password, password):
        flash("Введённый пароль неправильный.")
        return redirect(url_for('auth.login'))

    user.id_post = get_max_id(Posts)
    db.session.commit()

    login_user(user, remember=True)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        flash("Выйдите из аккаунта для регистрации нового.")
        return redirect(url_for('main.index'))
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    login = request.form.get('login')
    password = request.form.get('password')
    is_admin = request.form.get('admin_checkbox')
    if 'avatar' not in request.files:
        flash('Произошла ошибка с полем загрузки аватарки. Пожалуйста, перезагрузите страницу.')
        return redirect(url_for('auth.signup'))
    file = request.files['avatar']

    if len(login) <= 3 or len(login) > 20:
        flash("Логин должен быть длиной 4-20 символов.")
        return redirect(url_for('auth.signup'))

    user = Users.query.filter_by(login=login).first()

    if user:
        flash("Логин [{}] уже существует.".format(login))
        return redirect(url_for('auth.signup'))

    filename = file.filename
    if file:
        if allowed_extention(filename):
            app = create_app()
            if os.path.exists(app.static_folder+'/avatars/'+filename):
                filename = get_new_name_file(filename, app, '/avatars/')
            file.save(os.path.join(app.static_folder+'/avatars/', filename))
        else:
            flash("Загружаемая аватарка должна быть расширением: .png, .jpeg, .jpg.")
            return redirect(url_for('auth.signup'))
    else:
        filename = 'original.jpg'

    if is_admin == "on":
        key = request.form.get('admincode')
        app = create_app()
        if not check_password_hash(app.config['SECRET_KEY'], key):
            flash('Введённый секретный ключ для админского аккаунта не подходит.')
            return redirect(url_for('auth.signup'))

    max_id = get_max_id(Users)
    new_id = max_id+1 if max_id else 1
    new_user = Users(id=new_id,
            login=login,
            password=generate_password_hash(password, method='pbkdf2'),
            avatar_path=filename,
            id_post=get_max_id(Posts),
            is_admin=(is_admin == "on"))

    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)
    return redirect(url_for('main.index'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
