import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from userprofile.models import Profile
from .models import Expense, ExpenseChoices, ExpenseEntry, ExpensePaymentStatus
from .views import ExpenseRecordView, ExpenseListView
from utils import UrlUtils

class ExpenseViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = Profile.objects.create(first_name="User1", username="User1", email="user1@example.com")
        self.user2 = Profile.objects.create(first_name="User2", username="User2", email="user2@example.com")

    def test_create_expense_record(self):
        url = reverse(UrlUtils.EXPENSE_RECORD)
        data = {
            "name": "Test Expense",
            "expense_type": ExpenseChoices.EQUALLY,
            "paid_by": self.user1.id,
            "amount": 100.0,
            "split_data": [
                {"user": self.user1.id, "share": 50.0},
                {"user": self.user2.id, "share": 50.0}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_expense_list(self):
        url = reverse(UrlUtils.EXPENSE_LIST)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ExpenseViewsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create test users
        self.user1 = Profile.objects.create(username="User1", first_name="User1")
        self.user2 = Profile.objects.create(username="User2", first_name="User2")
        self.user3 = Profile.objects.create(username="User3", first_name="User3")

    def test_create_exact_expense_with_unequal_amount(self):
        # Test creating an exact expense
        data = {
            "name": "Exact Expense",
            "expense_type": ExpenseChoices.EXACT,
            "paid_by": self.user1.id,
            "amount": 100.0,
            "split_data": [{"user": self.user1.id, "share": 40.0}, {"user": self.user2.id, "share": 30.0}],
        }
        request = self.factory.post("/api/record/", json.dumps(data), content_type="application/json")
        response = ExpenseRecordView.as_view()(request)

        self.assertEqual(response.status_code, 400)

    def test_create_exact_expense_with_equal_amount(self):
        # Test creating an exact expense
        data = {
            "name": "Exact Expense",
            "expense_type": ExpenseChoices.EXACT,
            "paid_by": self.user1.id,
            "amount": 100.0,
            "split_data": [{"user": self.user1.id, "share": 70.0}, {"user": self.user2.id, "share": 30.0}],
        }
        request = self.factory.post("/api/record/", json.dumps(data), content_type="application/json")
        response = ExpenseRecordView.as_view()(request)

        self.assertEqual(response.status_code, 201)

    def test_create_percent_expense(self):
        # Test creating a percent expense
        data = {
            "name": "Percent Expense",
            "expense_type": ExpenseChoices.PERCENTAGE,
            "paid_by": self.user1.id,
            "amount": 100.0,
            "split_data": [{"user": self.user1.id, "share": 50.0}, {"user": self.user2.id, "share": 50.0}],
        }
        request = self.factory.post("/api/record/", json.dumps(data), content_type="application/json")
        response = ExpenseRecordView.as_view()(request)

        self.assertEqual(response.status_code, 201)

    def test_create_equal_expense(self):
        # Test creating an equal expense
        data = {
            "name": "Equal Expense",
            "expense_type": ExpenseChoices.EQUALLY,
            "paid_by": self.user1.id,
            "amount": 100.0,
            "split_data": [{"user": self.user1.id, "share": 33.34}, 
                           {"user": self.user2.id, "share": 33.33}, 
                           {"user": self.user3.id, "share": 33.33}],
        }
        request = self.factory.post("/api/record/", json.dumps(data), content_type="application/json")
        response = ExpenseRecordView.as_view()(request)

        self.assertEqual(response.status_code, 201)

    def test_list_expenses(self):
        # Test listing expenses
        expense = Expense.objects.create(name="Test Expense", expense_type=ExpenseChoices.EQUALLY, paid_by=self.user1, amount=100.0)
        expense.involved.add(self.user1, self.user2, self.user3)
        ExpenseEntry.objects.create(expense=expense, user=self.user1, share=33.34, status=ExpensePaymentStatus.PAID)
        ExpenseEntry.objects.create(expense=expense, user=self.user2, share=33.33)
        ExpenseEntry.objects.create(expense=expense, user=self.user3, share=33.33)

        request = self.factory.get("/api/expenses/list/")
        response = ExpenseListView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["expenses"]), 1)

    def test_list_individual_expenses(self):
        # Test listing individual expenses
        expense1 = Expense.objects.create(name="Expense 1", expense_type=ExpenseChoices.EQUALLY, paid_by=self.user1, amount=100.0)
        expense1.involved.add(self.user1, self.user2, self.user3)
        ExpenseEntry.objects.create(expense=expense1, user=self.user1, share=33.34, status=ExpensePaymentStatus.PAID)
        ExpenseEntry.objects.create(expense=expense1, user=self.user2, share=33.33)
        ExpenseEntry.objects.create(expense=expense1, user=self.user3, share=33.33)

        expense2 = Expense.objects.create(name="Expense 2", expense_type=ExpenseChoices.EQUALLY, paid_by=self.user2, amount=50.0)
        expense2.involved.add(self.user1, self.user2)
        ExpenseEntry.objects.create(expense=expense2, user=self.user1, share=25.0)
        ExpenseEntry.objects.create(expense=expense2, user=self.user2, share=25.0, status=ExpensePaymentStatus.PAID)

        request = self.factory.get("/api/expense/list/{}/".format(self.user1.id))
        response = ExpenseListView.as_view()(request, user_id=self.user1.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["expenses"]), 2)
