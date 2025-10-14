from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from documents.models import Document
from .serializers import DocumentSerializer, DocumentListSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document CRUD operations"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['trip', 'document_type']
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'title']
    ordering = ['-uploaded_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        return DocumentSerializer
    
    def get_queryset(self):
        """Return documents for trips owned by current user"""
        return Document.objects.filter(trip__user=self.request.user)
    
    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=True, methods=['delete'])
    def delete_file(self, request, pk=None):
        """Delete document file"""
        document = self.get_object()
        if document.file:
            document.file.delete()
            document.delete()
            return Response({'message': 'Document deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'No file found'}, status=status.HTTP_404_NOT_FOUND)