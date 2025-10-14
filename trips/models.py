from django.db import models
from django.conf import settings

class Trip(models.Model):
    """Trip model for storing travel plans"""
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('INR', 'Indian Rupee (₹)'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')  # NEW FIELD
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trips'
        ordering = ['-created_at']
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'
    
    def __str__(self):
        return f"{self.title} - {self.destination}"
    
    @property
    def duration_days(self):
        """Calculate trip duration in days"""
        return (self.end_date - self.start_date).days + 1

    def get_currency_symbol(self):
        """Get currency symbol"""
        return '$' if self.currency == 'USD' else '₹'