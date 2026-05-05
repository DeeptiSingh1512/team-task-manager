# Team Task Manager

A full-stack web application where teams can manage projects, assign tasks, and track progress. It supports two roles — Admin and Member — with different levels of access.

---

## Live Demo

https://team-task-manager-1-bgi7.onrender.com

> **Note:** Render is used for deployment since Railway’s free tier limit was exceeded, ensuring the app remains live and accessible.

## GitHub Repository

https://github.com/DeeptiSingh1512/team-task-manager

---

## What this app does

- Users can sign up and log in securely
- Admins can create projects and add team members
- Tasks can be created, assigned to members, and tracked by status
- Each task has a priority level (high, medium, low) and a due date
- The dashboard shows a summary of all tasks — how many are done, in progress, or overdue
- Overdue tasks are highlighted so nothing gets missed
- Members have limited access — they cannot create or delete projects and tasks

---

## Tech Stack

- Backend: Python 3, Flask
- Database: SQLite (local), PostgreSQL (production)
- ORM: Flask-SQLAlchemy
- Auth: Flask-Login, Flask-Bcrypt
- Frontend: HTML, CSS, Bootstrap 5
- Deployed on: Render

---

## How to run locally

1. Clone the repo

git clone https://github.com/DeeptiSingh1512/team-task-manager.git
cd team-task-manager

2. Create and activate virtual environment

python -m venv venv

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Create a .env file with the following

SECRET_KEY=your-secret-key-here

5. Run the app

python run.py

Then open http://127.0.0.1:5000 in your browser.

---

## Database Models

User — stores username, email, hashed password, and role
Project — belongs to a user (owner), has many tasks and members
ProjectMember — links users to projects with a role
Task — belongs to a project, can be assigned to a user, has status and due date

---

## Role-Based Access

Feature            Admin     Member
Create Project     Yes       No
Delete Project     Yes       No
Add Members        Yes       No
Create Task        Yes       Yes
Update Status      Yes       Yes
Delete Task        Yes       No
View Dashboard     Yes       Yes

---

## Project Structure

team-task-manager/
    app/
        __init__.py
        models.py
        auth/
        main/
        projects/
        tasks/
        templates/
        static/
    config.py
    run.py
    requirements.txt
    Procfile
    runtime.txt

---

## API Endpoints

Method    Endpoint                          Description
GET/POST  /signup                           Register new user
GET/POST  /login                            Login
GET       /logout                           Logout
GET       /dashboard                        Dashboard
GET       /projects                         List projects
GET/POST  /projects/create                  Create project (Admin)
GET       /projects/<id>                    View project
POST      /projects/<id>/delete             Delete project (Admin)
POST      /projects/<id>/add_member         Add member (Admin)
GET/POST  /projects/<id>/tasks/create       Create task
POST      /tasks/<id>/update_status         Update task status
POST      /tasks/<id>/delete                Delete task (Admin)

---

## Deployment Note

This project was originally assigned to be deployed on Railway. However, Railway's free tier limit was exceeded during development. The application has been deployed on Render as an alternative, and all features are fully functional on the live URL.

---

## Author

Deepti Singh
GitHub: https://github.com/DeeptiSingh1512