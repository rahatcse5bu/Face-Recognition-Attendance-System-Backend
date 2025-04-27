
# urls.py (api app)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, AttendanceViewSet, SettingsViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'settings', SettingsViewSet, basename='settings')

urlpatterns = [
    path('', include(router.urls)),
]