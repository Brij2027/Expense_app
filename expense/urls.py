from django.urls import path

from .views import ExpenseRecordView, ExpenseListView
from utils import UrlUtils

urlpatterns = [
    path("record/", ExpenseRecordView.as_view(), name=UrlUtils.EXPENSE_RECORD),
    path("expenses/list/", ExpenseListView.as_view(), name=UrlUtils.EXPENSE_LIST),
    path("expense/list/<int:user_id>/", ExpenseListView.as_view(), name=UrlUtils.EXPENSE_LIST_INDIVIDUAL),
]