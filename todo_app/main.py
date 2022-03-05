from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .ent import Task
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    todo_list = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', name=current_user.name, todo_list=todo_list)

@main.route('/add_task')
@login_required
def add_task():
    return render_template('create_task.html')

@main.route('/add_task', methods=['POST'])
@login_required
def add_task_post():

    title = request.form.get('title')
    content = request.form.get('content')

    new_task = Task(title=title,
                    content=content,
                    user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('main.profile'))

@main.route('/task/<int:task_id>/upate', methods=['GET', 'POST'])
@login_required
def update_task(task_id):

    task = Task.query.filter_by(id=task_id).first()
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.content = request.form.get('content')
        task.upd_dt = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('main.profile'))
    
    return render_template('update_task.html', task=task)

@main.route('/task/<int:task_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.profile'))
