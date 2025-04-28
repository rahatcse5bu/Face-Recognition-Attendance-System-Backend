# admin.py
from django.contrib import admin
from .models import Profile, Attendance, Settings

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'reg_number', 'is_active', 'registration_date')
    search_fields = ('name', 'email', 'reg_number')
    list_filter = ('is_active',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'date', 'time_in', 'time_out')
    list_filter = ('date',)
    search_fields = ('profile__name',)

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'esp32_url', 'dark_mode') 