import os
import sys
import subprocess
import platform

def check_compatibility():
    """Basic compatibility check"""
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Django 3.2 requires the 'cgi' module which was removed in Python 3.11+
    if python_version.major == 3 and python_version.minor >= 11:
        print("\nWARNING: You're using Python 3.11+ which is not compatible with Django 3.2")
        print("The 'cgi' module was removed in Python 3.11, but Django 3.2 still uses it.")
        print("\nTo make this work, you need to:")
        print("1. Install Python 3.9 or 3.10")
        print("2. Create a virtual environment with that Python version")
        print("3. Install the dependencies and run the server")
        print("\nExample commands:")
        print("python3.9 -m venv venv")
        print("venv\\Scripts\\activate  # On Windows")
        print("source venv/bin/activate  # On Linux/Mac")
        print("pip install -r requirements.txt")
        print("cd attendance_system")
        print("python manage.py makemigrations api")
        print("python manage.py migrate")
        print("python manage.py createsuperuser")
        print("python manage.py runserver")
        return False
    
    try:
        import django
        print(f"Django version: {django.__version__}")
    except ImportError:
        print("Django not found. Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        except Exception as e:
            print(f"Error installing dependencies: {e}")
            print("\nTRY THIS: Install the dependencies manually:")
            print("pip install Django==3.2.22 djangorestframework==3.12.4 djangorestframework-simplejwt==5.2.2 django-cors-headers==3.13.0")
            return False
    
    return True

def setup_project():
    """Setup the Django project"""
    os.chdir('attendance_system')
    
    # Initialize database
    try:
        print("Creating database migrations...")
        subprocess.check_call([sys.executable, "manage.py", "makemigrations", "api"])
        
        print("Applying migrations...")
        subprocess.check_call([sys.executable, "manage.py", "migrate"])
        
        # Create admin user
        print("Creating admin user...")
        create_superuser_cmd = (
            "from django.contrib.auth.models import User; "
            "User.objects.filter(username='admin').exists() or "
            "User.objects.create_superuser('admin', 'admin@example.com', 'admin');"
        )
        
        subprocess.check_call([
            sys.executable, "manage.py", "shell", "-c",
            create_superuser_cmd
        ])
        
        return True
    except Exception as e:
        print(f"Error setting up project: {e}")
        return False

def run_server():
    """Run the Django server"""
    print("\n=====================================================")
    print("Django server starting at http://127.0.0.1:8000/")
    print("Admin credentials: username='admin', password='admin'")
    print("Health check endpoint: http://127.0.0.1:8000/api/settings/health_check/")
    print("=====================================================\n")
    
    try:
        subprocess.check_call([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error running server: {e}")

if __name__ == "__main__":
    print("=== Attendance System Setup ===")
    
    if check_compatibility():
        if setup_project():
            run_server() 