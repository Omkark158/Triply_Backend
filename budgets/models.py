from django.db import models
from django.conf import settings
from trips.models import Trip

class Expense(models.Model):
    """Expense tracking for personal and group trips"""

    CATEGORY_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('food', 'Food & Dining'),
        ('transport', 'Transportation'),
        ('activities', 'Activities'),
        ('shopping', 'Shopping'),
        ('entertainment', 'Entertainment'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    ]

    EXPENSE_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('group', 'Group'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES, default='personal')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses_paid', null=True)
    split_between = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='expenses_shared')
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'expenses'
        ordering = ['-date', '-created_at']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        currency_symbol = self.trip.get_currency_symbol()
        return f"{self.title} - {currency_symbol}{self.amount} ({self.expense_type})"

    def split_amount(self):
        """Returns the per-person amount for group expenses"""
        if self.expense_type == 'group':
            count = self.split_between.count() or 1
            return self.amount / count
        return self.amount

    def get_currency(self):
        """Get currency from trip"""
        return self.trip.currency


class Budget(models.Model):
    """Budget tracking for trips"""
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('INR', 'Indian Rupee (₹)'),
    ]

    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name='budget_tracking')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'budgets'
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        currency_symbol = '$' if self.currency == 'USD' else '₹'
        return f"Budget for {self.trip.title} - {currency_symbol}{self.total_budget}"

    @property
    def spent_amount(self):
        """Calculate total spent from expenses"""
        return self.trip.expenses.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    @property
    def remaining_amount(self):
        """Calculate remaining budget"""
        return self.total_budget - self.spent_amount

    @property
    def spent_percentage(self):
        """Calculate percentage of budget spent"""
        if self.total_budget == 0:
            return 0
        return (self.spent_amount / self.total_budget) * 100

    def get_currency_symbol(self):
        """Get currency symbol"""
        return '$' if self.currency == 'USD' else '₹'