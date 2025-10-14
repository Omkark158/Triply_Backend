from django.db import models
from trips.models import Trip

class Destination(models.Model):
    """Destinations within a trip"""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='destinations')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    day_number = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'destinations'
        ordering = ['day_number', 'created_at']
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'
        unique_together = ['trip', 'day_number']  # Only one destination per day per trip
    
    def __str__(self):
        return f"{self.name} - Day {self.day_number}"


class Activity(models.Model):
    """Activities at each destination"""
    CATEGORY_CHOICES = [
        ('sightseeing', 'Sightseeing'),
        ('food', 'Food & Dining'),
        ('adventure', 'Adventure'),
        ('relaxation', 'Relaxation'),
        ('shopping', 'Shopping'),
        ('entertainment', 'Entertainment'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ]
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    booking_url = models.URLField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activities'
        ordering = ['start_time', 'created_at']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.title} at {self.destination.name}"

    def get_currency(self):
        """Get currency from trip via destination"""
        return self.destination.trip.currency

    def get_cost_with_currency(self):
        """Get formatted cost with currency symbol"""
        currency_symbol = self.destination.trip.get_currency_symbol()
        return f"{currency_symbol}{self.estimated_cost}"