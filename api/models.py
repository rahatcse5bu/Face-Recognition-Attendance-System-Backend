# Now let's create the API app

# models.py
from django.db import models
from django.contrib.auth.models import User
import json

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    reg_number = models.CharField(max_length=50, unique=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profiles/')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    face_encoding = models.TextField(blank=True, null=True)  # Stored as JSON string
    
    def __str__(self):
        return self.name
    
    def set_face_encoding(self, encoding_array):
        """Convert numpy array to JSON string for storage"""
        if encoding_array is not None:
            # Convert numpy array to list first
            self.face_encoding = json.dumps(encoding_array.tolist() if hasattr(encoding_array, 'tolist') else list(encoding_array))
    
    def get_face_encoding(self):
        """Get stored face encoding"""
        if self.face_encoding:
            return json.loads(self.face_encoding)
        return None

class Attendance(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ['profile', 'date']
    
    def __str__(self):
        return f"{self.profile.name} - {self.date}"

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    esp32_url = models.CharField(max_length=200, blank=True, null=True)
    dark_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Settings for {self.user.username}"
