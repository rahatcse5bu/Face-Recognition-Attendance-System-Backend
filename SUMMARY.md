# Attendance System API - Summary

This project is a Django-based REST API for an attendance tracking system that uses face recognition. It's designed to allow organizations to track attendance by identifying registered individuals through facial recognition.

## Project Structure

The project is organized as follows:

- `attendance_system/` - Main Django project directory
- `api/` - Django app containing the API functionality
  - `models.py` - Database models for Profile, Attendance, and Settings
  - `views.py` - ViewSets and API endpoints for the business logic
  - `serializers.py` - Serializers for the API responses
  - `face_recognition_utils.py` - Utilities for face recognition (mocked in this version)
  - `urls.py` - URL routing for the API endpoints

## Features

- **User Management**: Create and manage user profiles with personal information
- **Face Recognition**: Register and identify users by their facial features (simulated)
- **Attendance Tracking**: Record time-in and time-out
- **Reporting**: Generate daily and summary attendance reports
- **JWT Authentication**: Secure API access with token-based authentication

## Technical Implementation

- **Framework**: Django 3.2 with Django REST Framework
- **Database**: SQLite by default (can be switched to MongoDB)
- **Authentication**: JWT (JSON Web Tokens) via djangorestframework-simplejwt
- **CORS Support**: Cross-Origin Resource Sharing enabled

## Compatibility Notes

The system uses Django 3.2 which has compatibility issues with Python 3.11+ due to the removal of the `cgi` module. For production use, it's recommended to:

1. Use Python 3.9 or 3.10
2. Set up a virtual environment 
3. Install dependencies via requirements.txt

## Getting Started

See the README.md file for detailed setup instructions. The simplest approach is to:

1. Install Python 3.9 or 3.10
2. Create a virtual environment
3. Run the start.py script which will check compatibility and set up the project

## API Endpoints

The API provides several endpoints for managing the attendance system:

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

## Notes for Production Use

- The current implementation uses a mocked face recognition system. For real face recognition, install the `face-recognition` package and update the `face_recognition_utils.py` file.
- For production deployment, consider:
  - Using a more robust database like PostgreSQL
  - Setting DEBUG=False in settings.py
  - Implementing proper HTTPS with a valid SSL certificate
  - Restricting CORS settings to known domains 