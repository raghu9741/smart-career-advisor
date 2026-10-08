# 🎯 Smart Career Advisor

An AI-inspired career guidance and job recommendation platform designed to help students discover suitable career paths, understand required skills, explore job opportunities, and track their career development.

🌐 **Live Application:**  
https://smart-career-advisor-1.onrender.com
---

## 📌 Overview

**Smart Career Advisor** is a full-stack career guidance web application built using **Python Flask, PostgreSQL, HTML, CSS, and JavaScript**.

The platform provides students with:

- 🔐 User registration and login
- 👤 Student profile management
- 🎯 Career recommendations
- 💼 Job recommendations
- 📊 Career and skill information
- 📝 Feedback submission
- 🔑 Admin authentication
- 👨‍💼 Admin dashboard
- 📋 Career management
- 💼 Job listing management
- 📈 Login activity tracking
- 🗄️ PostgreSQL database support
- 🚀 Cloud deployment using Render

The application is designed as a practical project for students looking to understand how a complete web application works from frontend to backend and database.

---

# ✨ Features

## 👨‍🎓 Student Features

### 🔐 Authentication

Students can:

- Create an account
- Login
- Logout
- Maintain a user session using browser storage
- Receive validation messages for incorrect credentials

### 🎯 Career Recommendation

Students can explore career options based on their interests, branch, skills, and preferences.

Example career paths include:

- Software Developer
- Data Analyst
- AI Engineer
- Cybersecurity Analyst
- Cloud Engineer
- Web Developer
- Project Manager
- System Administrator

### 💼 Job Recommendations

The application provides job-related information including:

- Job role
- Company
- Location
- Eligibility
- Salary information
- Required skills

### 📝 Feedback

Students can submit feedback through the application.

---

# 👨‍💼 Admin Features

The application contains an administrative dashboard.

Administrators can:

- 🔐 Login securely
- 📊 View application statistics
- 👥 Monitor user activity
- 📈 View login activity
- 💼 Add jobs
- ✏️ Update jobs
- 🗑️ Delete jobs
- 🎯 Add careers
- ✏️ Update careers
- 🗑️ Delete careers
- 📝 View feedback
- 🗑️ Delete feedback

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       Student        │
                    │   Web Browser        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ HTML / CSS / JS      │
                    │ Frontend             │
                    └──────────┬───────────┘
                               │
                         HTTP / REST API
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Flask Backend     │
                    │      Python          │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ PostgreSQL       │        │ External Job API │
       │ Database         │        │ RapidAPI         │
       └──────────────────┘        └──────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Responsive UI
- Browser Local Storage

## Backend

- Python
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy
- Gunicorn

## Database

- PostgreSQL
- SQLite for local development

## APIs

- REST API
- RapidAPI / JSearch

## Deployment

- Docker
- Render
- GitHub

---

# 📂 Project Structure

```text
smart-career-advisor/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── admin_routes.py
│   ├── career_routes.py
│   ├── feedback_routes.py
│   ├── job_routes.py
│   ├── student_routes.py
│   ├── seed.py
│   ├── reset_admin.py
│   │
│   └── migrations/
│       ├── alembic.ini
│       ├── env.py
│       └── versions/
│
├── smart-career-advisor/
│   └── smart-c-advisor/
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── admin.html
│       ├── about.html
│       │
│       ├── script.js
│       ├── login.js
│       ├── register.js
│       ├── admin.js
│       ├── logout.js
│       │
│       ├── *.css
│       │
│       └── data/
│           ├── careers.json
│           └── jobs.json
│
├── Dockerfile
├── start.sh
├── requirements.txt
├── render.yaml
├── .env.example
├── .gitignore
└── README.md
```

---

# 🚀 Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-career-advisor.git
cd smart-career-advisor
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file or configure the variables in your terminal.

Example:

```env
FLASK_APP=backend.app

SCA_DATABASE_URI=sqlite:///backend/career_advisor.db

SCA_ADMIN_USERNAME=admin

SCA_ADMIN_PASSWORD=change-me

RAPIDAPI_KEY=your_rapidapi_key

RAPIDAPI_HOST=jsearch.p.rapidapi.com
```

⚠️ **Never commit your `.env` file or API keys to GitHub.**

---

## 5. Run the application

```bash
python backend/app.py
```

The application will normally run at:

```text
http://127.0.0.1:5000
```

Open:

```text
http://127.0.0.1:5000
```

or:

```text
http://127.0.0.1:5000/login.html
```

---

# 🐳 Run Using Docker

Build the Docker image:

```bash
docker build -t smart-career-advisor .
```

Run the container:

```bash
docker run -p 8000:10000 smart-career-advisor
```

Open:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# ☁️ Deploy to Render

The project includes:

```text
Dockerfile
render.yaml
start.sh
```

so it can be deployed directly to Render.

## Method 1 — Deploy Using Render Blueprint

1. Push the project to GitHub.

2. Open Render.

3. Create a new **Blueprint**.

4. Connect your GitHub repository.

5. Render detects:

```text
render.yaml
```

6. Review the services and database.

7. Enter the required secret values:

```text
SCA_ADMIN_USERNAME
SCA_ADMIN_PASSWORD
RAPIDAPI_KEY
```

8. Deploy the Blueprint.

Render will create the web service and PostgreSQL database defined in the Blueprint.

---

# 🔐 Render Environment Variables

Configure:

| Variable | Value |
|---|---|
| `FLASK_APP` | `backend.app` |
| `SCA_DATABASE_URI` | Render PostgreSQL connection |
| `SCA_ADMIN_USERNAME` | Your admin username |
| `SCA_ADMIN_PASSWORD` | Strong admin password |
| `RAPIDAPI_KEY` | Your RapidAPI key |
| `RAPIDAPI_HOST` | `jsearch.p.rapidapi.com` |

Do not put secret values directly inside GitHub.

---

# 🏥 Health Check

After deployment, test:

```text
https://YOUR-SERVICE.onrender.com/health
```

Expected:

```json
{
  "status": "ok"
}
```

Your current live service can be tested at:

https://smart-career-advisor-1.onrender.com/health

---

# 🌐 Application URLs

After deployment:

```text
Homepage
https://YOUR-SERVICE.onrender.com/

Login
https://YOUR-SERVICE.onrender.com/login.html

Registration
https://YOUR-SERVICE.onrender.com/register.html

Admin
https://YOUR-SERVICE.onrender.com/admin.html

Health
https://YOUR-SERVICE.onrender.com/health
```

Current deployed application:

```text
https://smart-career-advisor-1.onrender.com/login.html
```

---

# 🔑 Admin Login

The admin account is created using environment variables:

```text
SCA_ADMIN_USERNAME
SCA_ADMIN_PASSWORD
```

For example:

```text
Username: admin
Password: YOUR_SECURE_PASSWORD
```

Do not publish the actual admin password in this README.

---

# 🔄 Database Migrations

The application uses **Flask-Migrate / Alembic**.

The Render startup script automatically runs:

```bash
python -m flask --app backend.app db upgrade -d backend/migrations
```

before starting Gunicorn.

Then the application starts using:

```bash
gunicorn --bind 0.0.0.0:$PORT backend.app:app
```

---

# 📡 API Endpoints

## Authentication

### Register

```http
POST /register
```

Example:

```json
{
  "username": "student",
  "email": "student@example.com",
  "password": "password123"
}
```

### Login

```http
POST /login
```

### Logout

```http
POST /logout
```

---

## Health

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Career API

Career endpoints are available under:

```text
/api
```

The backend manages career information through the career routes.

---

## Job API

Job-related endpoints are available under:

```text
/api
```

The application can integrate job information through RapidAPI/JSearch.

---

# 🔒 Security

The application includes:

- Password hashing using Werkzeug
- Environment-based secrets
- PostgreSQL support
- CORS configuration
- Admin authentication
- Database migrations
- API validation
- Protected admin functionality

### Production recommendations

For a production application, consider adding:

- CSRF protection
- JWT/session-based authentication
- Rate limiting
- Secure cookies
- HTTPS-only cookies
- Stronger password requirements
- Input sanitization
- Role-based authorization
- Secret key configuration
- Production logging
- Security headers

---

# 📊 Main Modules

```text
Authentication
      │
      ├── Registration
      ├── Login
      └── Logout
            │
            ▼
      Student Dashboard
            │
      ┌─────┴─────┐
      │           │
      ▼           ▼
   Careers       Jobs
      │           │
      └─────┬─────┘
            ▼
       Career Guidance
            │
            ▼
         Feedback


Admin
  │
  ├── Statistics
  ├── Users/Login Activity
  ├── Careers
  ├── Jobs
  └── Feedback
```

---

# 🎯 Project Objectives

The main objectives of Smart Career Advisor are:

1. Help students identify suitable career paths.
2. Provide career and skill information.
3. Help students explore job opportunities.
4. Provide a centralized career guidance platform.
5. Allow administrators to manage career and job information.
6. Provide a foundation for future AI-powered career recommendations.

---

# 🔮 Future Enhancements

Potential future improvements include:

- 🤖 AI-powered career recommendations
- 📄 AI resume analysis
- 🧠 Skill gap analysis
- 🎤 AI mock interviews
- 📊 Student career analytics
- 📚 Personalized learning paths
- 🔗 LinkedIn/GitHub profile analysis
- 📈 Job-market trend analysis
- 🧑‍💼 Recruiter dashboard
- 📱 Android mobile application
- 🔔 Job alerts
- 🧠 Machine-learning based career prediction
- ☁️ Advanced cloud infrastructure

---

# 👨‍💻 Author

Developed as an academic and portfolio project focused on:

```text
Python
Flask
Web Development
Database Management
Career Guidance
REST APIs
Cloud Deployment
```

---

# ⭐ Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature/new-feature
```

3. Make your changes.
4. Commit:

```bash
git add .
git commit -m "Add new feature"
```

5. Push:

```bash
git push origin feature/new-feature
```

6. Create a Pull Request.

---

# 📜 License

This project is intended for educational and portfolio purposes.

---

## 🌐 Live Demo

**Smart Career Advisor**

https://smart-career-advisor-1.onrender.com/login.html

---

⭐ If you find this project useful, consider giving the repository a star!
