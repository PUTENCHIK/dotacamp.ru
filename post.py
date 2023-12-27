import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user
#from flask_login import login_required, current_user, login_user, logout_user
from .models import Users, Posts, Scores
from . import db, create_app
from .funcs import allowed_extention, get_new_name_file, get_max_id, get_previous_id

post = Blueprint('post', __name__)

@post.route('/create')
def create():
    if not current_user.is_authenticated:
        flash("Авторизируйтесь для создания постов.")
        return redirect(url_for('main.index'))
    return render_template('newpost.html')

@post.route('/create', methods=['POST'])
def create_post():
    text = request.form.get('create_post_text')
    if not text:
        flash('Для публикации поста необходимо заполнить текстовое поле.')
        return redirect(url_for('post.create'))

    if 'create_post_upload' not in request.files:
        flash('Произошла ошибка с полем загрузки картинки. Пожалуйста, перезагрузите страницу.')
        return redirect(url_for('post.create'))
    file = request.files['create_post_upload']
    filename = file.filename
    if file:
        if allowed_extention(filename):
            app = create_app()
            if os.path.exists(app.static_folder+'/pictures/'+filename):
                filename = get_new_name_file(filename, app, '/pictures/')
            file.save(os.path.join(app.static_folder+'/pictures/', filename))
        else:
            flash("Загружаемая картинка должна быть расширением: .png, .jpeg, .jpg.")
            return redirect(url_for('post.create'))
    else:
        filename = 'advert.jpg'

    max_id = get_max_id(Posts)
    new_id = max_id+1 if max_id else 1

    current_user.id_post = new_id
    new_post = Posts(id=new_id, id_author=current_user.id, text=text, img_path=filename)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('main.index'))

@post.route('/score', methods=['POST'])
def score():
    if current_user.is_authenticated:
        score = Scores.query.filter_by(id_user=current_user.id, id_post=current_user.id_post).first()
        if score:
            if (score.score == 1 and 'like' in request.form) or (score.score == 2 and 'dislike' in request.form):
                score.score = 0
            else:
                score.score = 1 if 'like' in request.form else 2
            db.session.commit()
        else:
            max_id = get_max_id(Scores)
            new_id = max_id+1 if max_id else 1
            new_score = Scores(id=new_id, id_user=current_user.id, id_post=current_user.id_post, score=(1 if 'like' in request.form else 2))
            db.session.add(new_score)
            db.session.commit()
    else:
        flash('Для оценки постов вам необходимо авторизоваться.')
    return redirect(url_for('main.index'))

@post.route('/edit')
def edit():
    if not current_user.is_authenticated:
        flash("Авторизуйтесь для редактирования постов.")
        return redirect(url_for('auth.login'))
    current_post = Posts.query.get(current_user.id_post)
    return render_template('edit.html', text=current_post.text)

@post.route('/edit', methods=['POST'])
def edit_post():
    text = request.form.get('create_post_text')

    if 'create_post_upload' not in request.files:
        flash('Произошла ошибка с полем загрузки картинки. Пожалуйста, перезагрузите страницу.')
        return redirect(url_for('post.edit'))
    file = request.files['create_post_upload']
    filename = file.filename
    
    post = Posts.query.get(current_user.id_post)
    if not post:
        flash("Редактируемый пост не найден")
        return redirect(url_for('main.index'))
    if file and filename:
        if allowed_extention(filename):
            app = create_app()
            if os.path.exists(app.static_folder+'/pictures/'+filename):
                filename = get_new_name_file(filename, app, '/pictures/')
            file.save(os.path.join(app.static_folder+'/pictures/', filename))

            if post.img_path != "advert.jpg":
                os.remove(app.static_folder + "/pictures/" + post.img_path)
        else:
            flash("Загружаемая картинка должна быть расширением: .png, .jpeg, .jpg.")
            return redirect(url_for('post.create'))

    if text:
        post.text = text
    if filename:
        post.img_path = filename
    db.session.commit()

    return redirect(url_for('main.index'))


@post.route('/delete')
def delete():
    if current_user.is_authenticated:
        if current_user.id_post:
            Scores.query.filter_by(id_post=current_user.id_post).delete()

            post = Posts.query.filter_by(id = current_user.id_post).first()
            app = create_app()
            if post.img_path != "advert.jpg":
                os.remove(app.static_folder + "/pictures/" + post.img_path)
            Posts.query.filter_by(id = current_user.id_post).delete()

            previous_id = get_previous_id(current_user.id_post, Posts)
            current_user.id_post = previous_id if previous_id else get_next_id(current_user.id_post, Posts)
            db.session.commit()
        else:
            flask("Попытка удаления несуществующего поста.")
    else:
        flask("Для удаления поста необходима авторизация.")
    return redirect(url_for('main.index'))
