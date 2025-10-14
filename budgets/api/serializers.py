from rest_framework import serializers
from budgets.models import Expense
from django.db.models import Sum

class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model"""
    paid_by = serializers.StringRelatedField(read_only=True)  # Shows user email or username

    class Meta:
        model = Expense
        fields = [
            'id', 'trip', 'paid_by', 'title', 'description', 'amount', 'category',
            'date', 'receipt_image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'paid_by']


class BudgetSummarySerializer(serializers.Serializer):
    """Serializer for budget summary"""
    total_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    remaining = serializers.DecimalField(max_digits=12, decimal_places=2)
    percentage_used = serializers.FloatField()
    expenses_by_category = serializers.DictField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
