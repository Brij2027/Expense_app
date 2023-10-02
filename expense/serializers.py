from rest_framework.serializers import ModelSerializer, ListField, FloatField
from django.core.exceptions import ValidationError

from .models import Expense, ExpenseEntry, ExpenseChoices

class ExpenseSerializer(ModelSerializer):
    shares = ListField(child=FloatField(), write_only=True)

    class Meta:
        model = Expense
        fields = "__all__"

    def validate(self, data):
        # Validate amount, expense type, and shares
        amount = data.get('amount', 0)
        expense_type = data.get('expense_type')
        shares = self.initial_data.get('shares', [])

        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        if expense_type not in [ExpenseChoices.EQUALLY, ExpenseChoices.EXACT, ExpenseChoices.PERCENTAGE]:
            raise ValidationError("Invalid expense type.")

        if expense_type == ExpenseChoices.PERCENTAGE:
            total_percent = sum(shares)
            if total_percent != 100:
                raise ValidationError("Total percentage shares must equal 100%.")

        if expense_type == ExpenseChoices.EXACT:
            total_shares = sum(shares)
            if total_shares != amount:
                raise ValidationError("Total shares must equal the total amount.")

        return data
    
    def create(self, validated_data):
        # Extract shares from validated data, but don't save them
        shares = validated_data.pop('shares', [])

        # Create the expense object without shares
        expense = Expense.objects.create(**validated_data)

        # Calculate and add shares as an extra field to the serialized data
        expense.shares = shares

        return expense

class ExpenseEntrySerializer(ModelSerializer):
    class Meta:
        model = ExpenseEntry
        fields = '__all__'

