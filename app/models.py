from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80),  unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    role       = db.Column(db.String(20),  nullable=False, default='member')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owned_projects = db.relationship('Project', backref='owner', lazy=True)
    assigned_tasks = db.relationship('Task',    backref='assignee', lazy=True, foreign_keys='Task.assigned_to')
    memberships    = db.relationship('ProjectMember', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Project(db.Model):
    __tablename__ = 'projects'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    owner_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    tasks   = db.relationship('Task',          backref='project', lazy=True, cascade='all, delete-orphan')
    members = db.relationship('ProjectMember', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'


class ProjectMember(db.Model):
    __tablename__ = 'project_members'

    id         = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    role       = db.Column(db.String(20), nullable=False, default='member')
    joined_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProjectMember user={self.user_id} project={self.project_id}>'


class Task(db.Model):
    __tablename__ = 'tasks'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status      = db.Column(db.String(20),  nullable=False, default='todo')
    priority    = db.Column(db.String(20),  nullable=False, default='medium')
    due_date    = db.Column(db.DateTime, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    project_id  = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=True)
    created_by  = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)

    creator = db.relationship('User', foreign_keys=[created_by], backref='created_tasks')

    def is_overdue(self):
        if self.due_date and self.status != 'done':
            return datetime.utcnow() > self.due_date
        return False

    def __repr__(self):
        return f'<Task {self.title} [{self.status}]>'