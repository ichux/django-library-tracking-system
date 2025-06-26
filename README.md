# 📚 Library Tracking System

Welcome to the **Library Tracking System**! This project is a comprehensive application built with **Python**, **Django**, **Django REST Framework (DRF)**, and **Celery**. It manages authors, books, members, and loans within a library context. The application is fully containerized using **Docker**, allowing for easy setup and deployment.

---

## 📌 **Project Overview**
This application enables **library tracking** by allowing users to manage authors, books, members, and loans efficiently.

### **Tech Stack**
- **Python 3.12.10** – Backend development.
- **Django 4.2** – Web framework.
- **Django REST Framework** – API development.
- **Celery 5.5.3** – Task queue for async jobs.
- **Redis 6** – Message broker for Celery.
- **PostgreSQL 17** – Database.
- **Docker & Docker Compose** – Containerized setup.

---

## 🛠 **Setup Instructions**

### 1️⃣ **Clone the Repository**
```sh
git clone https://gitlab.com/search-atlas-interviews/django-library-tracking-system
cd django-library-tracking-system
```

### 2️⃣ **Configure Your Git Remote**
To work with your own repository, you need to replace the default remote with one you control. We recommend using **GitHub** for this, it's free.

#### 🏗 **Create an Empty Public Repository on GitHub**
1. Go to [GitHub](https://github.com/) and sign in.
2. Click on the **+** in the top-right corner and select **New repository**.
3. Enter a repository name (e.g., `django-library-tracking-system`).
4. Choose **Public**.
5. **Do not** initialize with a README, `.gitignore`, or license.
6. Click **Create repository**.
7. Copy the repository URL (it should look like `https://github.com/your-username/your-repo.git`).

#### 🔧 **Replace the Default Git Remote**
Run the following commands to rename the existing remote and add your newly created repository:

```sh
git remote rename origin upstream
git remote add origin [YOUR_GITHUB_REPOSITORY_URL]
git push -u origin main
```

### 3️⃣ **Create a `.env` File**
Create a `.env` file in the root directory to store environment variables:
```sh
make e
```

#### 📌 **Content of `.env`**
```env
DEBUG=1
DJANGO_ALLOWED_HOSTS='localhost 127.0.0.1 [::1]'

# DB
DB_HOST=cf_lib_db
DB_PORT=5432
POSTGRES_TEST_DB=test_library_db
POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=library_password

# celery
CELERY_BROKER_URL=redis://cf_lib_redis:6379/0
CELERY_RESULT_BACKEND=redis://cf_lib_redis:6379/0

# misc
SECRET_KEY=c2c0126bd4139d0a2b7
DEFAULT_FROM_EMAIL=admin@library.com
DEFAULT_LOAN_PERIOD_DAYS=14

# this has to be the value of 'echo $(whoami)'
PC_USER=
```
> **Note:** Replace `c2c0126bd4139d0a2b7` with a secure key.

### 4️⃣ **Build and Run Docker Containers**
```sh
make b
```
This command will:
- Start PostgreSQL (`db`) and Redis (`redis`) services.
- Build and run the Django application (`web`).
- Run the Celery worker (`celery`).

### 5️⃣ **Initialize the Django Project**
Apply migrations and create a superuser:
```sh
make a
```
Follow the prompts to create a superuser account.

### 6️⃣ **Start the Application**
```sh
make e b
```
To stop the running containers, press `CTRL+C` in the terminal where `docker-compose up` is running, then execute:
```sh
docker compose down
```

---

## 📂 **Project Structure**
```plaintext
django-library-tracking-system/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── .gitignore
├── manage.py
├── library_system/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── library/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── tasks.py
    ├── tests.py
    └── views.py
```

---

## 📌 **Accessing the Application**

### 🔑 **Django Admin Interface**
- **URL:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Login:** Use the superuser credentials you created.
- **Functionality:** Manage authors, books, members, and loans through the admin panel.

### 📌 **API Endpoints**
| Method | Endpoint          | Description |
|--------|------------------|-------------|
| `GET`  | `/api/authors/`  | Fetch all authors |
| `GET`  | `/api/books/`    | Fetch all books |
| `GET`  | `/api/members/`  | Fetch all members |
| `GET`  | `/api/loans/`    | Fetch all loans |
| `POST` | `/api/authors/`  | Create a new author |
| `POST` | `/api/books/`    | Create a new book |
| `POST` | `/api/members/`  | Create a new member |
| `POST` | `/api/loans/`    | Create a new loan |

---

## 🎯 **License**
This project is licensed under the **MIT License**.

---

🚀 **Happy coding!** 🎉