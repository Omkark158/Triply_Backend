from rest_framework import serializers
from documents.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    file_extension = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'trip', 'title', 'document_type', 'file', 'file_url',
            'description', 'file_size', 'file_size_mb', 'file_extension',
            'uploaded_at'
        ]
        read_only_fields = ['id', 'file_size', 'uploaded_at']
    
    def get_file_url(self, obj):
        """Get full file URL"""
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def validate_file(self, value):
        """Validate file size (max 10MB)"""
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 10MB")
        return value

class DocumentListSerializer(serializers.ModelSerializer):
    """Lighter serializer for document lists"""
    file_extension = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'document_type', 'file_size_mb', 'file_extension', 'uploaded_at']