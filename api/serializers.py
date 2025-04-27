# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Attendance, Settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'email', 'blood_group', 'reg_number', 
                  'university', 'image', 'registration_date', 'is_active']
        read_only_fields = ['registration_date']

class AttendanceSerializer(serializers.ModelSerializer):
    profile_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = ['id', 'profile', 'profile_name', 'date', 'time_in', 'time_out']
        read_only_fields = ['date', 'time_in']
    
    def get_profile_name(self, obj):
        return obj.profile.name

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'esp32_url', 'dark_mode']
