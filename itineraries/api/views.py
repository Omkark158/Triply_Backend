from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from itineraries.models import Destination, Activity
from .serializers import (
    DestinationSerializer, DestinationListSerializer, ActivitySerializer
)

class DestinationViewSet(viewsets.ModelViewSet):
    """ViewSet for Destination CRUD operations"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['trip', 'day_number']
    search_fields = ['name', 'address']
    ordering_fields = ['day_number', 'created_at']
    ordering = ['day_number']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DestinationListSerializer
        return DestinationSerializer
    
    def get_queryset(self):
        """Return destinations for trips owned by current user"""
        return Destination.objects.filter(trip__user=self.request.user)

class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity CRUD operations"""
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['destination', 'category', 'is_completed']
    search_fields = ['title', 'description']
    ordering_fields = ['start_time', 'created_at']
    ordering = ['start_time']
    
    def get_queryset(self):
        """Return activities for destinations in trips owned by current user"""
        return Activity.objects.filter(destination__trip__user=self.request.user)