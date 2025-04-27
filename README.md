# Attendance System with Face Recognition API

A Django-based REST API for managing attendance using face recognition.

## Features

- Face recognition-based attendance tracking (simulated in this version)
- Profile management
- Attendance reporting (daily and summary)
- JWT authentication

## Important: Python Version Compatibility

This system uses Django 3.2 which is **not compatible** with Python 3.11 or higher due to the removal of the `cgi` module. Please use Python 3.9 or 3.10 for the best experience.

## Quick Start (Recommended)

Run the compatibility check script:

```bash
python start.py
```

If you have a compatible Python version, this will:
1. Install dependencies
2. Set up the database
3. Create an admin user
4. Start the server

## Manual Setup with Virtual Environment

```bash
# Create a virtual environment (use Python 3.9 or 3.10)
python3.9 -m venv venv

# Activate the environment
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup the database
cd attendance_system
python manage.py makemigrations api
python manage.py migrate

# Create admin user
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# Run the server
python manage.py runserver
```

## API Endpoints

- Health Check: `GET /api/settings/health_check/`
- Authentication: 
  - `POST /api/token/` (obtain token)
  - `POST /api/token/refresh/` (refresh token)
- Profiles:
  - `GET/POST /api/profiles/`
  - `GET/PUT/DELETE /api/profiles/{id}/`
  - `POST /api/profiles/register_with_face/`
  - `POST /api/profiles/{id}/update_face/`
- Attendance:
  - `GET/POST /api/attendance/`
  - `GET/PUT/DELETE /api/attendance/{id}/`
  - `POST /api/attendance/mark_attendance/`
  - `GET /api/attendance/reports/`
- Settings:
  - `GET /api/settings/my_settings/`
  - `PUT/PATCH /api/settings/update_settings/`
  - `POST /api/settings/test_esp32/`

## Notes

- Default admin credentials: username: `admin`, password: `admin`
- This version uses simulated face recognition - real face recognition features would require additional setup 