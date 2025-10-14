from django.contrib import admin
from .models import TripCollaborator, TripInvitation

@admin.register(TripCollaborator)
class TripCollaboratorAdmin(admin.ModelAdmin):
    list_display = ['user', 'trip', 'role', 'added_at']
    list_filter = ['role', 'added_at']
    search_fields = ['user__email', 'trip__title']

@admin.register(TripInvitation)
class TripInvitationAdmin(admin.ModelAdmin):
    list_display = ['invitee_email', 'trip', 'inviter', 'role', 'status', 'created_at', 'expires_at']
    list_filter = ['status', 'role', 'created_at']
    search_fields = ['invitee_email', 'trip__title', 'inviter__email']
    readonly_fields = ['token', 'created_at']