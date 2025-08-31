# Recipe Manager

A full-stack web application for creating, organizing, and sharing recipes. Built with **Django REST Framework** and **TypeScript + Webpack frontend**, it provides a platform for personal recipe management and discovery.

> **Development Status**: This project is paused and not actively maintained.

## Table of Contents

- [Demos](#demos)
- [Screenshots](#screenshots)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [License](#license)

## Demos

#### Recipe Create Page

![Recipe Create Demo](assets/recipe-create.gif)

#### Password Reset Page

![Password Reset Demo](assets/password-reset.gif)

## Screenshots

#### Login Page

![Login](assets/login.png)

#### Registration Page

![Register](assets/register.png)

#### Reset Password Page

![Reset Password](assets/reset-password.png)

#### Coming Soon Page

![Coming Soon](assets/coming-soon.png)

#### Feedback Page

![Feedback](assets/feedback.png)

#### Site Map Page

![Site Map](assets/site-map.png)

## Features

#### Backend API

**User Management**

- User registration & authentication
- Google OAuth integration
- Account activation via email
- Profile management & account deletion
- Login/logout functionality
- Password reset system via email
- Email notifications (via `django-allauth`)

**Recipe Management**

- Full CRUD (create, read, update, delete)
- Recipe listing with admin moderation
- Random recipe discovery
- Soft delete & restore support
- Recipe export capabilities
- Reporting & banning system
- Like/unlike functionality
- Recipe statistics & analytics

**Tag System**

- Create & manage tags
- Tag suggestions
- Full CRUD operations

**Testing**

- REST API coverage with Pytest

#### Frontend

**Authentication & User Flows**

- User registration & login pages
- User logout functionality
- Google OAuth integration
- Password reset & confirmation pages

**Recipe Management**

- Recipe creation interface

**UI & Navigation**

- Coming soon & feedback pages
- Site map navigation

## Technology Stack

**Backend**

- Django
- Django REST Framework
- SQLite database
- Pytest
- django-allauth
- django-environ

**Frontend**

- TypeScript
- Webpack
- SCSS
- HTML5

## Quick Start

#### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-raw.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

**Optional:**

```bash
python manage.py createsuperuser  # Create admin user
pytest apps/recipes/ apps/users/  # Run tests
```

#### Frontend Setup

```bash
cd frontend/webpack
npm install
npm run build:dev
```

#### .env Configuration

Copy the `.env.example` file to `.env` and update the values as needed.

```bash
# .env.example:
DEBUG=True
SECRET_KEY='django-insecure-code'
ALLOWED_HOSTS=localhost,127.0.0.1

FRONTEND_AFTER_GOOGLE_LOGIN_URL='http://127.0.0.1:8000/api/users/me/'
ACTIVATION_LINK_URL='http://0.0.0.0:8000/auth/activate/'
PASSWORD_RESET_URL='http://0.0.0.0:8000/api/auth/password-reset/'

GOOGLE_OAUTH2_CLIENT_ID=''
GOOGLE_OAUTH2_CLIENT_SECRET=''
GOOGLE_OAUTH2_CALLBACK_URL='http://127.0.0.1:8000/api/auth/google/callback/'  # URL where Google redirects after login

EMAIL_HOST_USER=''      # The email address to send from ('your-email@example.com')
EMAIL_HOST_PASSWORD=''  # The email provider's app-specific password or SMTP password
```

## License

This project is licensed under the MIT [LICENSE](LICENSE).
