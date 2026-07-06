# 🚀 FastAPI CRM System

A lightweight **CRM (Customer Relationship Management) system** built using **FastAPI, Jinja2, and SQLite**, with a clean UI powered by Tailwind CSS.

This project demonstrates backend API development, authentication, database design, and server-side rendered UI — making it perfect for showcasing full-stack Python skills.

---

## ✨ Features

- 🔐 User Authentication (Login / Logout)
- 👥 User Management
- 📊 Lead Management (Create, View)
- 🧾 Dashboard with all leads
- 🎨 Modern UI using Tailwind CSS
- ⚡ FastAPI backend (high performance)
- 🗄️ SQLite database (easy setup)

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Frontend:** Jinja2 Templates + Tailwind CSS
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Server:** Uvicorn / Gunicorn

---

## 📂 Project Structure
```
fastapi-crm/
│
├── routers/ # API routes
├── templates/ # HTML (Jinja2)
├── models.py # Database models
├── schemas.py # Pydantic schemas
├── database.py # DB connection
├── auth.py # Authentication logic
├── main.py # Entry point
├── crm.db # SQLite database
└── README.md

```
---

## ⚙️ Installation & Setup

### 1. Clone the repo
git clone https://github.com/Trupti840/fastapi-crm.git
cd fastapi-crm


### 2. Create virtual environment


python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows


### 3. Install dependencies


pip install -r requirements.txt


### 4. Run the server


uvicorn main:app --reload


---

## 🌐 Access the App

- Login Page → http://127.0.0.1:8000/login  
- Dashboard → http://127.0.0.1:8000/dashboard  

---

## 📸 Screenshots

_Add screenshots here (highly recommended for resume projects)_

---

## 🚀 Future Improvements

- ✏️ Edit & Delete Leads
- 📊 Analytics Dashboard
- 📧 Email Notifications
- 🤖 AI-based Lead Scoring
- 🔐 JWT Authentication
- 🌍 Deployment (Render / AWS)

---

## 💡 What I Learned

- Building REST APIs with FastAPI  
- Using Jinja2 for server-side rendering  
- Database modeling with SQLAlchemy  
- Authentication handling  
- Structuring scalable backend projects  

---

## 👩‍💻 Author

**Trupti Pawar**  
- GitHub: https://github.com/Trupti840  

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!
