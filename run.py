import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 11:
        print(f"WARNING: You're using Python {python_version.major}.{python_version.minor}")
        print("Django 4.2 may have issues with Python 3.11+ due to removed modules.")
        print("Consider using Python 3.9 or 3.10 for best compatibility.")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting. Please install Python 3.9 or 3.10.")
            sys.exit(1)

def install_dependencies():
    """Install dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully!")

def run_server():
    """Run the Django development server"""
    print("Starting Django development server...")
    # Change directory to where manage.py is located
    os.chdir('attendance_system')
    
    # Make migrations
    print("Creating database migrations...")
    subprocess.check_call([sys.executable, "manage.py", "makemigrations", "api"])
    
    # Apply migrations
    print("Applying migrations...")
    subprocess.check_call([sys.executable, "manage.py", "migrate"])
    
    # Create a superuser (admin) if it doesn't exist
    print("Ensuring admin user exists...")
    create_superuser_cmd = (
        "from django.contrib.auth.models import User; "
        "User.objects.filter(username='admin').exists() or "
        "User.objects.create_superuser('admin', 'admin@example.com', 'admin');"
    )
    
    subprocess.check_call([
        sys.executable, "manage.py", "shell", "-c",
        create_superuser_cmd
    ])
    
    # Run server
    print("\n=====================================================")
    print("Django server starting at http://127.0.0.1:8000/")
    print("Admin credentials: username='admin', password='admin'")
    print("Health check endpoint: http://127.0.0.1:8000/api/settings/health_check/")
    print("=====================================================\n")
    
    subprocess.check_call([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    try:
        # Check Python version
        check_python_version()
        
        # Install dependencies
        install_dependencies()
        
        # Run server
        run_server()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 