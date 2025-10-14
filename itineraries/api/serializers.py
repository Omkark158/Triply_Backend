from rest_framework import serializers
from itineraries.models import Destination, Activity

class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    class Meta:
        model = Activity
        fields = [
            'id', 'destination', 'title', 'description', 'category',
            'start_time', 'end_time', 'estimated_cost', 'booking_url',
            'is_completed', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class DestinationSerializer(serializers.ModelSerializer):
    """Serializer for Destination model"""
    activities = ActivitySerializer(many=True, read_only=True)
    activities_count = serializers.IntegerField(source='activities.count', read_only=True)
    
    class Meta:
        model = Destination
        fields = [
            'id', 'trip', 'name', 'address', 'latitude', 'longitude',
            'day_number', 'notes', 'activities', 'activities_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class DestinationListSerializer(serializers.ModelSerializer):
    """Lighter serializer for destination lists"""
    activities_count = serializers.IntegerField(source='activities.count', read_only=True)
    
    class Meta:
        model = Destination
        fields = ['id', 'name', 'day_number', 'activities_count', 'created_at']