# ALX Travel App

A real-world Django backend project that powers a travel listing platform. This project is built with industry-standard tools and practices to ensure scalability, maintainability, and team collaboration.

## 🌍 About the Project

The `alxtravelapp` project is a production-ready Django application that forms the foundation of a travel listing platform. This milestone is focused on:

- Setting up the Django project with modular configurations.
- Integrating MySQL as the relational database.
- Incorporating Swagger for API documentation.
- Applying best practices for environment configuration and dependency management.

This project is part of the ALX Software Engineering program and serves as a robust backend scaffold for building scalable APIs.

---

## 🎯 Learning Objectives

By completing this project, you will:

- **Master Advanced Project Initialization**
  - Structure Django projects for production use.
  - Use modular, scalable, and secure configurations.
  - Manage sensitive data using environment variables (`django-environ`).

- **Integrate Key Developer Tools**
  - Add Swagger via `drf-yasg` for API documentation.
  - Set up `django-cors-headers` for CORS configuration.
  - Configure MySQL as the default database backend.

- **Collaborate Effectively Using Git**
  - Maintain a clean Git-based workflow.
  - Push code to a remote GitHub repository with proper structure.

- **Adopt Industry Best Practices**
  - Structure your app into reusable components.
  - Follow separation of concerns and 12-factor app principles.

---

## ⚙️ Tech Stack

- **Backend Framework**: Django, Django REST Framework
- **Database**: MySQL
- **API Documentation**: Swagger (drf-yasg)
- **Task Queue (planned)**: Celery + RabbitMQ
- **Environment Configuration**: `django-environ`
- **CORS Management**: `django-cors-headers`

---

## 📦 Requirements
```bash
Python 3.8+
MySQL
RabbitMQ

# For Ubuntu-based systems (WSL/Linux):
sudo apt update
sudo apt install mysql-server libmysqlclient-dev pkg-config build-essential
```

---

## 🧾 requirements.txt
```
django
djangorestframework
django-cors-headers
django-environ
drf-yasg
mysqlclient
celery
```

---

## 🔍 Swagger UI
Once the server is running, access API documentation at:
```
http://localhost:8000/swagger/
```

## 🛠️ Project Structure

```bash
alxtravelapp/
├── alx_travel_app/        # Django project root
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── listings/              # Core app for travel listings
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── .env                   # Environment variables (not pushed to GitHub)
├── manage.py
├── requirements.txt
└── README.md
