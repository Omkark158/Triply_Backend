from django.db import models
from django.conf import settings
from trips.models import Trip
import os

def document_upload_path(instance, filename):
    """Generate upload path for documents"""
    return f'documents/user_{instance.trip.user.id}/trip_{instance.trip.id}/{filename}'

class Document(models.Model):
    """Document storage for trips"""
    DOCUMENT_TYPE_CHOICES = [
        ('passport', 'Passport'),
        ('visa', 'Visa'),
        ('ticket', 'Ticket/Boarding Pass'),
        ('booking', 'Booking Confirmation'),
        ('insurance', 'Travel Insurance'),
        ('itinerary', 'Itinerary'),
        ('map', 'Map'),
        ('other', 'Other'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to=document_upload_path)
    description = models.TextField(blank=True, null=True)
    file_size = models.IntegerField(help_text='File size in bytes', editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'documents'
        ordering = ['-uploaded_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
    
    def __str__(self):
        return f"{self.title} - {self.trip.title}"
    
    def save(self, *args, **kwargs):
        """Save file size on upload"""
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    @property
    def file_extension(self):
        """Get file extension"""
        return os.path.splitext(self.file.name)[1].lower()
    
    @property
    def file_size_mb(self):
        """Get file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)