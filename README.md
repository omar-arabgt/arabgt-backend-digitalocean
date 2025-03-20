# Django Dockerized Project

## Overview

This project is a **Django Application** designed with a modular architecture to handle different services. It integrates:

- **Django REST Framework** for mobile API endpoints
- **dj-rest-auth & allauth** for user registration and authentication
- **Django Templates** for the admin dashboard
- **External MySQL DB Integration** to fetch external data
- **PostgreSQL** as the primary database

## Project Structure

```
core/
├── .env.example          # Example environment variables file
├── asgi.py               # ASGI config
├── celery.py             # Celery config
├── routers.py            # DB routing (MySQL & PostgreSQL)
├── settings.py           # Django settings
├── urls.py               # Main URL routing
├── utils.py              # Utility functions
├── wsgi.py               # WSGI config
api/
├── migrations/
├── admin.py
├── apps.py
├── choices.py
├── filters.py
├── mixins.py
├── models.py
├── pagination.py
├── permissions.py
├── serializers.py
├── signals.py
├── tasks.py
├── tests.py
├── urls.py
├── utils.py
├── views.py
authentication/
├── adapter.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── tests.py
├── urls.py
├── views.py
news/
├── admin.py
├── apps.py
├── models.py
├── preprocessing.py
├── tasks.py
├── tests.py
├── urls.py
├── views.py
web/
├── migrations/
├── templatetags/
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
├── utils.py
├── views.py
locale/                    # Arabic translations
nginx/                     # Nginx configs and certificates
static/                    # Static files (CSS, JS, etc.)
templates/                 # HTML templates (per app)
ARABGT.postman_collection.json  # Postman collection for APIs
docker-compose.yml
docker-entrypoint.sh
Dockerfile
manage.py
README.md
requirements.txt
```

## Components

### 1. Api App
Handles API endpoints for mobile applications:
- Built using **Django REST Framework**
- Contains custom filters, pagination, permissions
- Includes Celery tasks for background processing
- Files like `choices.py`, `mixins.py`, `signals.py`, and `utils.py` promote reusable logic

### 2. Authentication App
Handles registration and authentication:
- Integrated with **dj-rest-auth** & **allauth**
- Custom `adapter.py` for custom password reset and confirmation mail.
- Provides API endpoints for login with email and social accounts, logout, password reset, etc.

### 3. Web App
Admin dashboard:
- Uses Django Templates
- Custom template tags and forms for enhanced UI experience

### 4. News App
Integrates with external MySQL DB:
- Reads external schema and writes usable processed data into PostgreSQL
- Contains `preprocessing.py` for data cleaning/formatting
- Periodic sync tasks handled via Celery

## Tech Stack

- **Python 3.x**
- **Django 4.x**
- **PostgreSQL (Primary DB)**
- **MySQL (Read-only external DB)**
- **Redis (Celery broker)**
- **Django REST Framework**
- **dj-rest-auth & allauth**
- **Docker & Docker Compose**
- **Nginx (Reverse Proxy, SSL certificates)**

## Setup


### 1. Environment Variables
- Copy the `.env.example` to `.env` and set your environment variables:
```bash
cp core/.env.example core/.env
```

### 2. Build & Run Docker Containers
```bash
docker-compose up --build
```

This will:
- Build Django app container
- Set up PostgreSQL, Redis, Nginx containers
- Run migrations, collect static files, and start servers


### 3. Access Points
- **Admin Dashboard:** `https://localhost:443/web/`
- **API Endpoints:** `https://localhost:443/api/`
- **Authentication Endpoints:** `https://localhost:443/auth/`

## Celery & Periodic Tasks

Celery handles background jobs such as:
- Reading data from the MySQL DB periodically (via `news.tasks`)
- Sending emails, notifications, etc.


## Translations

Arabic translations are stored in the `locale` directory. Update translations:
```bash
docker-compose exec arabgt_web django-admin makemessages -l ar
docker-compose exec arabgt_web django-admin compilemessages
```


## API Documentation

Use the provided **Postman collection**:
- File: `ARABGT.postman_collection.json`
- Import into Postman to access and test all available endpoints.


## Folder Highlights

| Folder/File               | Purpose                                         |
|--------------------------|-------------------------------------------------|
| **nginx/**               | Reverse proxy, SSL certs, custom Nginx config   |
| **static/**              | Static files (CSS/JS)                           |
| **templates/**           | HTML templates structured by app               |
| **docker-compose.yml**   | Docker service definitions                      |
| **docker-entrypoint.sh** | Entry point script for Django setup            |
| **Dockerfile**           | Builds the Django container                     |
| **requirements.txt**     | Python dependencies                            |
