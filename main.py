from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from .models import Users, Posts, Scores
from .funcs import get_max_id, get_min_id, index_obj
from . import db, create_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if not current_user.is_authenticated:
        flash("Просмотр ленты недоступен без авторизации.")
        return redirect(url_for('auth.login'))
    
    likes = sum([scr.score == 1 and scr.id_post == current_user.id_post for scr in Scores.query.all()])
    dislikes = sum([scr.score == 2 and scr.id_post == current_user.id_post for scr in Scores.query.all()])

    maybe_score = Scores.query.filter_by(id_post = current_user.id_post, id_user = current_user.id).first()
    if not maybe_score or not maybe_score.score:
        you_liked = you_disliked = False
    else:
       you_liked = True if maybe_score.score == 1 else False
       you_disliked = not you_liked

    return render_template('index.html', likes=likes, dislikes=dislikes, max_id=get_max_id(Posts), min_id=get_min_id(Posts), you_liked=you_liked, you_disliked=you_disliked, true_id=index_obj(current_user.id_post, Posts), posts_amount=len(Posts.query.all()), users=Users, posts=Posts)

