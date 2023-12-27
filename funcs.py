import os
from . import db

def get_max_id(table):
    ids = [row.id for row in table.query.all()]
    return max(ids) if ids else 0

def get_min_id(table):
    ids = [row.id for row in table.query.all()]
    return min(ids) if ids else 0

def get_previous_id(old, table):
    current = old-1
    while not table.query.get(current) and current > 0:
        current -= 1
    return current

def get_next_id(old, table):
    current = old+1
    max_id = get_max_id(table)
    while not table.query.get(current) and current <= max_id:
        current += 1
    return current if current <= max_id else 0

def index_obj(id, table):
    objs = table.query.all()
    current = 0
    for obj in objs:
        if obj.id == id: break
        current += 1
    return len(objs) - current

def allowed_extention(filename):
    allowed = ['png', 'jpg', 'jpeg']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def get_new_name_file(old, app, folder):
    name = old[:old.index('.')]
    extention = old[old.index('.'):]

    count = 1
    while os.path.exists(app.static_folder+folder+name + '-' + str(count) + extention):
        count += 1
    return name + '-' + str(count) + extention

