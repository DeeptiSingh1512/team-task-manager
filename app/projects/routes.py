from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Project, ProjectMember, User
from app.projects import projects


def is_admin():
    return current_user.role == 'admin'


@projects.route('/projects')
@login_required
def list_projects():
    if is_admin():
        all_projects = Project.query.all()
    else:
        memberships  = ProjectMember.query.filter_by(user_id=current_user.id).all()
        all_projects = [m.project for m in memberships]
    return render_template('projects/list.html', projects=all_projects)


@projects.route('/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if not is_admin():
        flash('Only admins can create projects.', 'danger')
        return redirect(url_for('projects.list_projects'))

    if request.method == 'POST':
        name        = request.form.get('name').strip()
        description = request.form.get('description').strip()

        if not name:
            flash('Project name is required.', 'danger')
            return redirect(url_for('projects.create_project'))

        project = Project(name=name, description=description, owner_id=current_user.id)
        db.session.add(project)
        db.session.commit()

        # Auto-add creator as admin member
        member = ProjectMember(project_id=project.id, user_id=current_user.id, role='admin')
        db.session.add(member)
        db.session.commit()

        flash(f'Project "{name}" created!', 'success')
        return redirect(url_for('projects.list_projects'))

    return render_template('projects/create.html')


@projects.route('/projects/<int:project_id>')
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    members = ProjectMember.query.filter_by(project_id=project_id).all()
    all_users = User.query.all()
    member_ids = [m.user_id for m in members]
    return render_template('projects/view.html', project=project,
                           members=members, all_users=all_users,
                           member_ids=member_ids)


@projects.route('/projects/<int:project_id>/add_member', methods=['POST'])
@login_required
def add_member(project_id):
    if not is_admin():
        flash('Only admins can add members.', 'danger')
        return redirect(url_for('projects.view_project', project_id=project_id))

    user_id = request.form.get('user_id')
    role    = request.form.get('role', 'member')

    existing = ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first()
    if existing:
        flash('User is already a member.', 'warning')
        return redirect(url_for('projects.view_project', project_id=project_id))

    member = ProjectMember(project_id=project_id, user_id=user_id, role=role)
    db.session.add(member)
    db.session.commit()
    flash('Member added!', 'success')
    return redirect(url_for('projects.view_project', project_id=project_id))


@projects.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    if not is_admin():
        flash('Only admins can delete projects.', 'danger')
        return redirect(url_for('projects.list_projects'))

    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'info')
    return redirect(url_for('projects.list_projects'))