from django.db import models
from django.conf import settings
from trips.models import Trip
import uuid

class TripCollaborator(models.Model):
    """Collaborators for trips"""
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='collaborators')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collaborative_trips')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'trip_collaborators'
        unique_together = ['trip', 'user']
        ordering = ['-added_at']
        verbose_name = 'Trip Collaborator'
        verbose_name_plural = 'Trip Collaborators'
    
    def __str__(self):
        return f"{self.user.email} - {self.trip.title} ({self.role})"

class TripInvitation(models.Model):
    """Invitations to collaborate on trips"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='invitations')
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
    invitee_email = models.EmailField()
    role = models.CharField(max_length=10, choices=TripCollaborator.ROLE_CHOICES, default='viewer')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'trip_invitations'
        ordering = ['-created_at']
        verbose_name = 'Trip Invitation'
        verbose_name_plural = 'Trip Invitations'
    
    def __str__(self):
        return f"Invitation to {self.invitee_email} for {self.trip.title}"
    
    @property
    def is_expired(self):
        """Check if invitation is expired"""
        from django.utils import timezone
        return timezone.now() > self.expires_at