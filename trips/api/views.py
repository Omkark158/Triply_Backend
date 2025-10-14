from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from trips.models import Trip
from .serializers import TripSerializer, TripListSerializer

class TripViewSet(viewsets.ModelViewSet):
    """ViewSet for Trip CRUD operations"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['destination', 'start_date', 'end_date']
    search_fields = ['title', 'destination', 'description']
    ordering_fields = ['start_date', 'created_at', 'budget']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TripListSerializer
        return TripSerializer
    
    def get_queryset(self):
        """Return trips for the current user"""
        return Trip.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating a trip"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming trips"""
        from django.utils import timezone
        upcoming_trips = self.get_queryset().filter(start_date__gte=timezone.now().date())
        serializer = self.get_serializer(upcoming_trips, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get past trips"""
        from django.utils import timezone
        past_trips = self.get_queryset().filter(end_date__lt=timezone.now().date())
        serializer = self.get_serializer(past_trips, many=True)
        return Response(serializer.data)