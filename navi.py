import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from .models import Users, Posts, Scores
from . import db, create_app
from .funcs import get_max_id, get_min_id, get_previous_id, get_next_id

navi = Blueprint('navi', __name__)

@navi.route('/previous')
def previous():
    previous_id = get_previous_id(current_user.id_post, Posts)
    current_user.id_post = previous_id if previous_id else current_user.id_post
    db.session.commit()
    return redirect(url_for('main.index'))

@navi.route('/next')
def next():
    next_id = get_next_id(current_user.id_post, Posts)
    current_user.id_post = next_id if next_id else current_user.id_post
    db.session.commit()
    return redirect(url_for('main.index'))

@navi.route('/first')
def first():
    current_user.id_post = get_max_id(Posts)
    db.session.commit()
    return redirect(url_for('main.index'))

@navi.route('/last')
def last():
    current_user.id_post = get_min_id(Posts)
    db.session.commit()
    return redirect(url_for('main.index'))
