from django.contrib import admin
from .models import Trip

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'user', 'start_date', 'end_date', 'budget', 'created_at']
    list_filter = ['start_date', 'end_date', 'is_public', 'created_at']
    search_fields = ['title', 'destination', 'user__email']
    date_hierarchy = 'start_date'
    ordering = ['-created_at']