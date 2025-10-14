from rest_framework import serializers
from trips.models import Trip

class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model"""
    duration_days = serializers.ReadOnlyField()
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'user', 'user_email', 'title', 'description', 
            'destination', 'start_date', 'end_date', 'budget', 
            'is_public', 'duration_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate that end_date is after start_date"""
        if data.get('start_date') and data.get('end_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("End date must be after start date")
        return data

class TripListSerializer(serializers.ModelSerializer):
    """Lighter serializer for trip lists"""
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Trip
        fields = ['id', 'title', 'destination', 'start_date', 'end_date', 'budget', 'duration_days', 'created_at']