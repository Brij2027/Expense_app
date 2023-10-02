from django.db import models
from userprofile.models import Profile

# Create your models here.
class ExpenseChoices:
    EQUALLY = "equally"
    EXACT = "exact"
    PERCENTAGE = "percentage"

    ExpenseChoice = [
        (EQUALLY, EQUALLY),
        (EXACT, EXACT),
        (PERCENTAGE,PERCENTAGE)
    ]

class ExpensePaymentStatus:
    PAID = "paid"
    DUE = "due"

    PaymentStatus = [
        (PAID, PAID),
        (DUE, DUE)
    ]

class Expense(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False)
    expense_type = models.CharField(choices=ExpenseChoices.ExpenseChoice, default=ExpenseChoices.EQUALLY, max_length=20)
    paid_by = models.ForeignKey(Profile, on_delete=models.ProtectedError, null=False, related_name='expenses_paid')
    involved = models.ManyToManyField(Profile, null=True, blank=True, related_name='expenses_involved')
    amount = models.FloatField(null=False)


class ExpenseEntry(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.ProtectedError, null=False)
    user = models.ForeignKey(Profile, on_delete=models.ProtectedError, null=False)
    share = models.FloatField(default=0.0)
    status = models.CharField(choices=ExpensePaymentStatus.PaymentStatus, default=ExpensePaymentStatus.DUE, max_length=4)
    


