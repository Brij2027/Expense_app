import json
from rest_framework.views import APIView, Request,status
from rest_framework.response import Response
from django.db.models.query import Q

from .serializers import ExpenseSerializer, ExpenseEntrySerializer
from userprofile.models import Profile
from .models import Expense, ExpenseChoices, ExpenseEntry, ExpensePaymentStatus

# Create your views here.

class ExpenseRecordView(APIView):

    def post(self, request: Request):
        data = json.loads(request.body)
        split_data = data.pop("split_data")
        data.update({"shares": [split.get("share") for split in split_data]})
        expenseserializer = ExpenseSerializer(data=data)
        if expenseserializer.is_valid(raise_exception=True):
            expenseserializer.save()
        #expenseentry 
        expense_data = expenseserializer.data
        expense = Expense.objects.get(pk=expense_data['id'])
        expense.involved.set([split.get("user") for split in split_data])
        for split in split_data:
            if expense.paid_by.id == split.get('user'):
                updation_dict = {"expense": expense_data['id'], "status": ExpensePaymentStatus.PAID}
            else: 
                updation_dict = {"expense": expense_data['id']}
            split.update(updation_dict) 
        
        expenseentryserializer = ExpenseEntrySerializer(data=split_data, many=True)
        if expenseentryserializer.is_valid(raise_exception=True):
            expenseentryserializer.save()
        return Response(data=json.dumps({"success":"true"}), status=status.HTTP_201_CREATED)
    
class ExpenseListView(APIView):
    def get_amount(self, total_amount, amount, expense_type, involved_count):
        if expense_type == ExpenseChoices.EQUALLY:
            return round(total_amount/ involved_count, 2)
        elif expense_type == ExpenseChoices.EXACT:
            return round(amount,2)
        else:
            return round((amount * total_amount) * 100, 2)


    def formatted_response(self, expense, entries, user, total_amount, type, involved_count=1):
        owes = []
        lended = []
        if entries:
            #check how much user owes and how much he has to give
            for entry in entries:
                data = {
                        "user": entry.user, 
                        "share": entry.share
                }
                if entry.expense.paid_by == user:
                    lended.append(data)
                elif entry.expense.paid_by != entry.user:
                    owes.append(data)
        return {
            expense : [
                f"{lent.get('user').first_name} owes {user.first_name} " 
                f"{self.get_amount(total_amount, lent.get('share'), type, involved_count)} amount" for lent in lended
            ] + [
                f"{user.first_name} owe {owe.get('user').first_name} "
                f"{self.get_amount(total_amount, owe.get('share'), type, involved_count)} amount" for owe in owes
            ]
        }
 
    def individual_expense_list(self, pk):
        user = Profile.objects.get(pk=pk)
        expenses = Expense.objects.filter(
            Q(paid_by=user) | Q(involved=user)
            ).distinct()
        resp = []
        for expense in expenses:
            entries = ExpenseEntry.objects.filter(expense=expense, status=ExpensePaymentStatus.DUE)
            resp.append(self.formatted_response(
                expense.name, entries, expense.paid_by, expense.amount, expense.expense_type, expense.involved.count()))
        return resp

    def get(self, request: Request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return Response({"expenses": self.individual_expense_list(user_id)}, status=status.HTTP_200_OK)
        
        resp = []
        for expense in Expense.objects.all():
            resp.append(self.formatted_response(
                expense.name,
                ExpenseEntry.objects.filter(expense=expense, status=ExpensePaymentStatus.DUE),
                expense.paid_by,
                expense.amount, 
                expense.expense_type, 
                expense.involved.count()
            ))
        return Response({"expenses":resp}, status=status.HTTP_200_OK)



            

        

