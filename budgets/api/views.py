from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from budgets.models import Expense
from trips.models import Trip
from .serializers import ExpenseSerializer, BudgetSummarySerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for Expense CRUD operations"""
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['trip', 'category', 'date']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        """Return expenses for trips owned by current user"""
        return Expense.objects.filter(trip__user=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='summary/(?P<trip_id>[^/.]+)')
    def trip_summary(self, request, trip_id=None):
        """Get budget summary for a specific trip"""
        try:
            trip = Trip.objects.get(id=trip_id, user=request.user)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=404)
        
        expenses = self.get_queryset().filter(trip=trip)
        total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        # Expenses by category
        expenses_by_category = {}
        for category, _ in Expense.CATEGORY_CHOICES:
            category_total = expenses.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
            expenses_by_category[category] = float(category_total)
        
        summary = {
            'total_budget': float(trip.budget),
            'total_spent': float(total_spent),
            'remaining': float(trip.budget - total_spent),
            'percentage_used': (float(total_spent) / float(trip.budget) * 100) if trip.budget > 0 else 0,
            'expenses_by_category': expenses_by_category
        }
        
        serializer = BudgetSummarySerializer(summary)
        return Response(serializer.data)