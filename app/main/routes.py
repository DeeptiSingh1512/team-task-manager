from flask import render_template
from flask_login import login_required, current_user
from datetime import datetime
from app.main import main
from app.models import Task, Project, ProjectMember


@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        all_projects = Project.query.all()
        all_tasks    = Task.query.all()
    else:
        memberships  = ProjectMember.query.filter_by(user_id=current_user.id).all()
        all_projects = [m.project for m in memberships]
        project_ids  = [p.id for p in all_projects]
        all_tasks    = Task.query.filter(Task.project_id.in_(project_ids)).all() if project_ids else []

    now = datetime.utcnow()

    total_tasks    = len(all_tasks)
    completed      = len([t for t in all_tasks if t.status == 'done'])
    in_progress    = len([t for t in all_tasks if t.status == 'in_progress'])
    todo           = len([t for t in all_tasks if t.status == 'todo'])
    overdue        = len([t for t in all_tasks if t.is_overdue()])

    recent_tasks   = sorted(all_tasks, key=lambda t: t.created_at, reverse=True)[:5]
    overdue_tasks  = [t for t in all_tasks if t.is_overdue()]

    return render_template('dashboard.html',
        all_projects=all_projects,
        total_tasks=total_tasks,
        completed=completed,
        in_progress=in_progress,
        todo=todo,
        overdue=overdue,
        recent_tasks=recent_tasks,
        overdue_tasks=overdue_tasks
    )