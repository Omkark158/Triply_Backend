from rest_framework import serializers
from collaboration.models import TripCollaborator, TripInvitation
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class CollaboratorSerializer(serializers.ModelSerializer):
    """Serializer for TripCollaborator"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TripCollaborator
        fields = ['id', 'trip', 'user', 'user_email', 'user_name', 'role', 'added_at']
        read_only_fields = ['id', 'added_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

class InvitationSerializer(serializers.ModelSerializer):
    """Serializer for TripInvitation"""
    inviter_email = serializers.EmailField(source='inviter.email', read_only=True)
    inviter_name = serializers.SerializerMethodField()
    trip_title = serializers.CharField(source='trip.title', read_only=True)
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = TripInvitation
        fields = [
            'id', 'trip', 'trip_title', 'inviter', 'inviter_email', 'inviter_name',
            'invitee_email', 'role', 'token', 'status', 'message',
            'created_at', 'expires_at', 'is_expired'
        ]
        read_only_fields = ['id', 'inviter', 'token', 'status', 'created_at']
    
    def get_inviter_name(self, obj):
        return f"{obj.inviter.first_name} {obj.inviter.last_name}".strip() or obj.inviter.username
    
    def create(self, validated_data):
        """Set inviter and expiration date"""
        validated_data['inviter'] = self.context['request'].user
        validated_data['expires_at'] = timezone.now() + timedelta(days=7)
        return super().create(validated_data)

class InvitationResponseSerializer(serializers.Serializer):
    """Serializer for accepting/declining invitations"""
    action = serializers.ChoiceField(choices=['accept', 'decline'])