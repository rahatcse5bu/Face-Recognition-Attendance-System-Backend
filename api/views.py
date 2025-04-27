# views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
import os
import cv2
from datetime import datetime, time, timedelta

from .models import Profile, Attendance, Settings
from .serializers import (
    ProfileSerializer, AttendanceSerializer, SettingsSerializer, UserSerializer
)
from .face_recognition_utils import (
    get_esp32_image, extract_face_encoding, recognize_face
)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    @action(detail=False, methods=['post'])
    def register_with_face(self, request):
        """Register a new profile with face recognition"""
        try:
            # Get profile data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Check if reg_number is unique
            reg_number = serializer.validated_data.get('reg_number')
            if Profile.objects.filter(reg_number=reg_number).exists():
                return Response({'error': 'Registration number already exists'}, 
                               status=status.HTTP_400_BAD_REQUEST)
            
            # Create profile
            profile = serializer.save()
            
            # Mock face encoding
            encoding, error = extract_face_encoding(None)
            if error:
                profile.delete()
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save encoding to profile
            profile.set_face_encoding(encoding)
            profile.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def update_face(self, request, pk=None):
        """Update face encoding for an existing profile"""
        profile = self.get_object()
        
        try:
            # Mock extract face encoding
            encoding, error = extract_face_encoding(None)
            if error:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save encoding to profile
            profile.set_face_encoding(encoding)
            profile.save()
            
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by date
        date_str = self.request.query_params.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(date=date_obj)
            except ValueError:
                pass
        
        # Filter by profile
        profile_id = self.request.query_params.get('profile_id')
        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def mark_attendance(self, request):
        """Mark attendance by face recognition"""
        try:
            # Get active profiles
            profiles = Profile.objects.filter(is_active=True)
            if not profiles:
                return Response({'error': 'No active profiles found'}, 
                               status=status.HTTP_400_BAD_REQUEST)
            
            # Mock image capture
            image = get_esp32_image(None)
            
            # Recognize face
            matches, error = recognize_face(image, profiles)
            if error:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
            # Process matches
            results = []
            for profile_id, face_location in matches:
                profile = Profile.objects.get(id=profile_id)
                
                # Check if attendance already marked for today
                today = timezone.now().date()
                attendance = Attendance.objects.filter(profile=profile, date=today).first()
                
                if attendance:
                    # Update time_out if attendance already exists
                    if not attendance.time_out:
                        attendance.time_out = timezone.now()
                        attendance.save()
                        results.append({
                            'profile_id': profile.id,
                            'name': profile.name,
                            'action': 'time_out',
                            'time': attendance.time_out
                        })
                else:
                    # Create new attendance record
                    attendance = Attendance.objects.create(profile=profile)
                    results.append({
                        'profile_id': profile.id,
                        'name': profile.name,
                        'action': 'time_in',
                        'time': attendance.time_in
                    })
            
            return Response({'results': results})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def reports(self, request):
        """Generate attendance reports"""
        try:
            report_type = request.query_params.get('type', 'daily')
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            profile_id = request.query_params.get('profile_id')
            
            # Parse dates
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            else:
                start_date = timezone.now().date()
            
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            else:
                end_date = start_date
            
            # Get base queryset
            queryset = Attendance.objects.all()
            
            # Apply filters
            if profile_id:
                queryset = queryset.filter(profile_id=profile_id)
            
            queryset = queryset.filter(date__gte=start_date, date__lte=end_date)
            
            # Generate report based on type
            if report_type == 'daily':
                # Daily report - just return filtered records
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            
            elif report_type == 'summary':
                # Summary report - aggregate by profile
                summary = []
                profiles = {}
                
                if profile_id:
                    profiles[profile_id] = get_object_or_404(Profile, id=profile_id).name
                else:
                    for profile in Profile.objects.all():
                        profiles[profile.id] = profile.name
                
                for profile_id, profile_name in profiles.items():
                    profile_records = queryset.filter(profile_id=profile_id)
                    total_days = (end_date - start_date).days + 1
                    present_days = profile_records.values('date').distinct().count()
                    
                    summary.append({
                        'profile_id': profile_id,
                        'name': profile_name,
                        'total_days': total_days,
                        'present_days': present_days,
                        'absent_days': total_days - present_days,
                        'attendance_percentage': (present_days / total_days * 100) if total_days > 0 else 0
                    })
                
                return Response(summary)
            
            else:
                return Response({'error': 'Invalid report type'}, 
                               status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SettingsViewSet(viewsets.ModelViewSet):
    serializer_class = SettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Settings.objects.filter(user=self.request.user)
    
    def get_object(self):
        # Get or create settings for current user
        settings, created = Settings.objects.get_or_create(user=self.request.user)
        return settings
    
    @action(detail=False, methods=['get'])
    def my_settings(self, request):
        settings = self.get_object()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def health_check(self, request):
        """Check if the API is working"""
        return Response({
            'status': 'healthy',
            'message': 'Attendance System API is running correctly'
        })
    
    @action(detail=False, methods=['put', 'patch'])
    def update_settings(self, request):
        settings = self.get_object()
        serializer = self.get_serializer(settings, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def test_esp32(self, request):
        """Test connection to ESP32 camera"""
        return Response({
            'success': True, 
            'message': 'Mock ESP32 camera connection successful'
        })