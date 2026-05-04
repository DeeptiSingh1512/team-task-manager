from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Task, Project, ProjectMember, User
from app.tasks import tasks


def is_admin():
    return current_user.role == 'admin'


def is_project_member(project_id):
    return ProjectMember.query.filter_by(
        project_id=project_id, user_id=current_user.id).first() is not None


@tasks.route('/projects/<int:project_id>/tasks')
@login_required
def list_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    if not is_admin() and not is_project_member(project_id):
        flash('Access denied.', 'danger')
        return redirect(url_for('projects.list_projects'))
    all_tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('tasks/list.html', project=project, tasks=all_tasks)


@tasks.route('/projects/<int:project_id>/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)
    if not is_admin() and not is_project_member(project_id):
        flash('Access denied.', 'danger')
        return redirect(url_for('projects.list_projects'))

    if request.method == 'POST':
        title       = request.form.get('title').strip()
        description = request.form.get('description').strip()
        priority    = request.form.get('priority', 'medium')
        assigned_to = request.form.get('assigned_to') or None
        due_date_str = request.form.get('due_date')

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

        if not title:
            flash('Task title is required.', 'danger')
            return redirect(url_for('tasks.create_task', project_id=project_id))

        task = Task(
            title=title, description=description,
            priority=priority, assigned_to=assigned_to,
            due_date=due_date, project_id=project_id,
            created_by=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created!', 'success')
        return redirect(url_for('tasks.list_tasks', project_id=project_id))

    members = ProjectMember.query.filter_by(project_id=project_id).all()
    return render_template('tasks/create.html', project=project, members=members)


@tasks.route('/tasks/<int:task_id>/update_status', methods=['POST'])
@login_required
def update_status(task_id):
    task   = Task.query.get_or_404(task_id)
    status = request.form.get('status')

    if status not in ['todo', 'in_progress', 'done']:
        flash('Invalid status.', 'danger')
        return redirect(url_for('tasks.list_tasks', project_id=task.project_id))

    task.status = status
    db.session.commit()
    flash('Task status updated!', 'success')
    return redirect(url_for('tasks.list_tasks', project_id=task.project_id))


@tasks.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not is_admin():
        flash('Only admins can delete tasks.', 'danger')
        return redirect(url_for('tasks.list_tasks', project_id=task.project_id))

    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'info')
    return redirect(url_for('tasks.list_tasks', project_id=project_id))