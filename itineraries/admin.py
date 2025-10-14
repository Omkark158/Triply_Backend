from django.contrib import admin
from .models import Destination, Activity

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1
    fields = ['title', 'category', 'start_time', 'end_time', 'estimated_cost', 'is_completed']

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'trip', 'day_number', 'created_at']
    list_filter = ['day_number', 'created_at']
    search_fields = ['name', 'trip__title']
    inlines = [ActivityInline]

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'category', 'start_time', 'estimated_cost', 'is_completed']
    list_filter = ['category', 'is_completed', 'created_at']
    search_fields = ['title', 'destination__name']