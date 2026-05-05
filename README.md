📌 Team Task Manager (Full-Stack Web App)
A full-stack web application to manage projects, assign tasks, and track progress with role-based access control.

🚀 Live Demo
👉 https://team-task-manager-1-bgi7.onrender.com

## 📝 Deployment Note

This project was assigned to be deployed on **Railway**, however Railway's free tier resource limit was exceeded. The application has been deployed on **Render** (free tier) as an alternative, and all features are **fully functional** on the live URL.

> Live URL: https://team-task-manager-1-bgi7.onrender.com

📂 GitHub Repository
View Source Code

✨ Features

🔐 User Authentication (Signup/Login)
👥 Role-Based Access (Admin / Member)
📁 Project Management
✅ Task Creation & Assignment
📊 Dashboard with:

Total Tasks
Completed Tasks
In-Progress Tasks
Overdue Tasks


📈 Progress Tracking
⚠️ Overdue Task Alerts


🛠️ Tech Stack
LayerTechnologyBackendPython 3, FlaskDatabaseSQLite (dev), PostgreSQL (prod)ORMFlask-SQLAlchemyAuthenticationFlask-Login, Flask-BcryptFrontendHTML, CSS, Bootstrap 5DeploymentRender

⚙️ Local Setup
1. Clone the repository
bashgit clone https://github.com/DeeptiSingh1512/team-task-manager.git
cd team-task-manager
2. Create virtual environment
bashpython -m venv venv

# Windows
venv\Scripts\activate

3. Install dependencies
bashpip install -r requirements.txt
4. Create .env file
SECRET_KEY=your-secret-key-here
5. Run the app
bashpython run.py
Visit http://127.0.0.1:5000 in your browser.

🗄️ Database Models
User
├── id, username, email, password, role, created_at
├── owns → Projects
└── assigned → Tasks

Project
├── id, name, description, owner_id, created_at
├── has → Tasks
└── has → ProjectMembers

ProjectMember
├── id, project_id, user_id, role, joined_at

Task
├── id, title, description, status, priority
├── due_date, created_at
├── project_id, assigned_to, created_by
└── is_overdue() → bool

🔐 Role-Based Access Control
FeatureAdminMemberCreate Project✅❌Delete Project✅❌Add Members✅❌Create Task✅✅Update Task Status✅✅Delete Task✅❌View Dashboard✅✅

📁 Project Structure
team-task-manager/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── auth/                # Authentication routes
│   ├── main/                # Dashboard routes
│   ├── projects/            # Project routes
│   ├── tasks/               # Task routes
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS assets
├── config.py                # App configuration
├── run.py                   # Entry point
├── Procfile                 # Deployment config
├── runtime.txt              # Python version
└── requirements.txt         # Dependencies

📊 API Endpoints
MethodEndpointDescriptionAccessGET/POST/signupRegister new userPublicGET/POST/loginLogin userPublicGET/logoutLogout userLogged inGET/dashboardView dashboardLogged inGET/projectsList projectsLogged inGET/POST/projects/createCreate projectAdminGET/projects/<id>View projectMemberPOST/projects/<id>/deleteDelete projectAdminPOST/projects/<id>/add_memberAdd memberAdminGET/POST/projects/<id>/tasks/createCreate taskMemberPOST/tasks/<id>/update_statusUpdate statusMemberPOST/tasks/<id>/deleteDelete taskAdmin

👩‍💻 Author
Deepti Singh

GitHub: @DeeptiSingh1512
