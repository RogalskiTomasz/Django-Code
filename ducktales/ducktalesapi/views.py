from math import floor
from .serializers import EditPatchExpenseSerializer, GetExpenseSerializer, GetPatchExpenseSerializer, \
    GetRecurringExpenseSerializer, InterestCalculatorRequestSerializer, AddExpenseSerializer, \
    AddRecurringExpenseSerializer, AddPatchExpenseSerializer
from rest_framework import views
from .calculators import zinsrechner
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PatchExpense, SingleExpense, RecurringExpense, Users
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# Create your views here.
@permission_classes([permissions.AllowAny])
class CalculatorView(views.APIView):
    def post(self, request):
        serializer = InterestCalculatorRequestSerializer(data=request.data)
        if serializer.is_valid():
            result = zinsrechner(float(serializer.data['starting_capital']),
                                 float(serializer.data['interest_rate']),
                                 serializer.data['unit'],
                                 int(serializer.data['duration']))
            return Response({"result": result}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Invalid request."}, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class SingleExpensePOST(views.APIView):
    def post(self, request):
        serializer = AddExpenseSerializer(data=request.data)
        if serializer.is_valid():
            current_user = Users.objects.get(email=request.user)
            single_expense = SingleExpense(user=current_user, name=serializer.data['name'],
                                           value=serializer.data['value'], sign=serializer.data['sign'],
                                           date=serializer.data['date'])
            single_expense.save()
            return Response({"result": "Yes"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Invalid request."}, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class PatchExpensePOST(views.APIView):
    def post(self, request):
        serializer = AddPatchExpenseSerializer(data=request.data)
        if serializer.is_valid():
            current_user = Users.objects.get(email=request.user)
            multiple_expense = RecurringExpense.objects.filter(user=current_user).get(id=serializer.data['id'])
            patch_expense = PatchExpense(user=current_user, rec_exp=multiple_expense, name=serializer.data['name'],
                                         value=serializer.data['value'], sign=serializer.data['sign'],
                                         index=serializer.data['index'])
            patch_expense.save()
            return Response({"result": "Yes"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Invalid request."}, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class SingleExpenseDELETE(views.APIView):
    def delete(self, request, id):
        SingleExpense.objects.filter(user=Users.objects.get(email=request.user)).filter(id=id).delete()
        response = {'result': True}
        return Response(response, status=status.HTTP_200_OK)

    def get(self, request, id):
        return Response(GetExpenseSerializer(
            SingleExpense.objects.filter(user=Users.objects.get(email=request.user)).get(id=id)).data)

    def post(self, request, id):
        serializer = AddExpenseSerializer(data=request.data)
        if serializer.is_valid():
            recurring_expense = SingleExpense.objects.filter(user=Users.objects.get(email=request.user)).get(id=id)
            recurring_expense.name = serializer.data['name']
            recurring_expense.value = serializer.data['value']
            recurring_expense.sign = serializer.data['sign']
            recurring_expense.date = serializer.data['date']
            recurring_expense.save()
        return Response({"result": "Yes"}, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class RecurringExpenseDELETE(views.APIView):
    def delete(self, request, id):
        RecurringExpense.objects.filter(user=Users.objects.get(email=request.user)).filter(id=id).delete()
        response = {'result': True}
        return Response(response, status=status.HTTP_200_OK)

    def get(self, request, id):
        return Response(GetRecurringExpenseSerializer(
            RecurringExpense.objects.filter(user=Users.objects.get(email=request.user)).get(id=id)).data)

    def post(self, request, id):
        serializer = AddRecurringExpenseSerializer(data=request.data)
        if serializer.is_valid():
            recurring_expense = RecurringExpense.objects.filter(user=Users.objects.get(email=request.user)).get(id=id)
            recurring_expense.name = serializer.data['name']
            recurring_expense.value = serializer.data['value']
            recurring_expense.sign = serializer.data['sign']
            recurring_expense.start_date = serializer.data['start_date']
            recurring_expense.end_date = serializer.data['end_date']
            recurring_expense.unit = serializer.data['unit']
            recurring_expense.save()
        return Response({"result": "Yes"}, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class PatchExpenseDELETE(views.APIView):
    def delete(self, request, id):
        PatchExpense.objects.filter(user=Users.objects.get(email=request.user)).filter(id=id).delete()
        response = {'result': True}
        return Response(response, status=status.HTTP_200_OK)

    def get(self, request, id):
        return Response(GetPatchExpenseSerializer(
            PatchExpense.objects.filter(user=Users.objects.get(email=request.user)).get(id=id)).data)

    def post(self, request, id):
        serializer = EditPatchExpenseSerializer(data=request.data)
        if serializer.is_valid():
            patch_expense = PatchExpense.objects.filter(user=Users.objects.get(email=request.user)).get(id=id)
            patch_expense.name = serializer.data['name']
            patch_expense.value = serializer.data['value']
            patch_expense.sign = serializer.data['sign']
            patch_expense.index = serializer.data['index']
            patch_expense.save()
        return Response({"result": "Yes"}, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class RecurringExpenseFromPatchExpense(views.APIView):
    def get(self, request, id):
        return Response(GetRecurringExpenseSerializer(RecurringExpense.objects.get(
            id=PatchExpense.objects.filter(user=Users.objects.get(email=request.user)).get(id=id).rec_exp.id)).data)


@permission_classes([permissions.IsAuthenticated])
class PatchExpensesFromRecurring(views.APIView):
    def get(self, request, id):
        return Response(GetPatchExpenseSerializer(
            PatchExpense.objects.filter(user=Users.objects.get(email=request.user)).filter(rec_exp_id=id),
            many=True).data)


@permission_classes([permissions.IsAuthenticated])
class SingleExpenseSumGET(views.APIView):
    def get(self, request):
        single_expenses = SingleExpense.objects.filter(user=Users.objects.get(email=request.user))
        single_expenses = single_expenses.filter(
            date__gte=request.query_params['start-date']) if "start-date" in request.query_params else single_expenses
        single_expenses = single_expenses.filter(
            date__lte=request.query_params['end-date']) if "end-date" in request.query_params else single_expenses
        sum = 0
        for se in single_expenses:
            if se.sign:
                sum += se.value
            else:
                sum -= se.value
        response = {'value': sum}
        return Response(response, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class MultipleExpenseSumGET(views.APIView):
    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    def get(self, request):
        multiple_expenses = RecurringExpense.objects.filter(user=Users.objects.get(email=request.user))
        multiple_expenses = multiple_expenses.filter(end_date__gte=request.query_params[
            'start-date']) if "start-date" in request.query_params else multiple_expenses
        multiple_expenses = multiple_expenses.filter(start_date__lte=request.query_params[
            'end-date']) if "end-date" in request.query_params else multiple_expenses
        sum = 0
        for multiple_expense in multiple_expenses:
            end_date_req = multiple_expense.end_date
            start_date_req = multiple_expense.start_date
            if "start-date" in request.query_params:
                start_date_req = datetime.strptime(request.query_params['start-date'],
                                                   '%Y-%m-%d').date() if datetime.strptime(
                    request.query_params['start-date'],
                    '%Y-%m-%d').date() > multiple_expense.start_date else multiple_expense.start_date
            if "end-date" in request.query_params:
                end_date_req = datetime.strptime(request.query_params['end-date'],
                                                 '%Y-%m-%d').date() if datetime.strptime(
                    request.query_params['end-date'],
                    '%Y-%m-%d').date() < multiple_expense.end_date else multiple_expense.end_date
            relativedelta_intermediate = relativedelta(end_date_req, start_date_req)
            time_range = end_date_req - start_date_req

            if multiple_expense.unit == "d":
                if multiple_expense.sign:
                    sum += time_range.days * multiple_expense.value
                else:
                    sum -= time_range.days * multiple_expense.value
            if multiple_expense.unit == "w":
                if multiple_expense.sign:
                    sum += floor(time_range.days / 7) * multiple_expense.value
                else:
                    sum -= floor(time_range.days / 7) * multiple_expense.value
            if multiple_expense.unit == "m":
                if multiple_expense.sign:
                    sum += (
                                       relativedelta_intermediate.months + relativedelta_intermediate.years * 12) * multiple_expense.value
                else:
                    sum -= (
                                       relativedelta_intermediate.months + relativedelta_intermediate.years * 12) * multiple_expense.value
            if multiple_expense.unit == "y":
                if multiple_expense.sign:
                    sum += relativedelta_intermediate.years * multiple_expense.value
                else:
                    sum -= relativedelta_intermediate.years * multiple_expense.value
        response = {'value': sum}
        return Response(response)


@permission_classes([permissions.IsAuthenticated])
class SingleExpenseGET(views.APIView):
    def get(self, request):
        return Response(single_expense_helper(request))


@permission_classes([permissions.IsAuthenticated])
class RecurringExpensePOST(views.APIView):
    def post(self, request):
        serializer = AddRecurringExpenseSerializer(data=request.data)
        if serializer.is_valid():
            current_user = Users.objects.get(email=request.user)
            recurring_expense = RecurringExpense(user=current_user, name=serializer.data['name'],
                                                 value=serializer.data['value'], sign=serializer.data['sign'],
                                                 start_date=serializer.data['start_date'],
                                                 end_date=serializer.data['end_date'], unit=serializer.data['unit'])
            recurring_expense.save()
            return Response({"result": "Yes"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Invalid request."}, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class AllExpensesGET(views.APIView):
    def get(self, request):
        return Response(single_expense_helper(request) + recurring_expense_helper(request))


@permission_classes([permissions.IsAuthenticated])
class AllExpensesGETLatest(views.APIView):
    def get(self, request):
        offset = int(request.query_params['offset'])
        number = int(request.query_params['number'])
        multiple_expenses = RecurringExpense.objects.filter(user=Users.objects.get(email=request.user)).order_by(
            '-created')[:number].values()
        single_expenses = SingleExpense.objects.filter(user=Users.objects.get(email=request.user)).order_by('-created')[
                          :number].values()
        patch_expenses = PatchExpense.objects.filter(user=Users.objects.get(email=request.user)).order_by('-created')[
                         :number].values()
        ret_array = [] + list(multiple_expenses) + list(single_expenses) + list(patch_expenses)
        ret_sorted = sorted(ret_array, key=lambda d: d['created'], reverse=True)[offset:number]

        return Response(ret_sorted)


@permission_classes([permissions.IsAuthenticated])
class RecurringExpenseGET(views.APIView):
    def get(self, request):
        return Response(recurring_expense_helper(request))


@permission_classes([permissions.IsAuthenticated])
class LogoutUserView(views.APIView):
    def post(self, request):
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"status": "Successful logout."}, status=status.HTTP_200_OK)


def single_expense_helper(request):
    single_expenses = SingleExpense.objects.filter(user=Users.objects.get(email=request.user))
    single_expenses = single_expenses.filter(
        date__gte=request.query_params['start-date']) if "start-date" in request.query_params else single_expenses
    single_expenses = single_expenses.filter(
        date__lte=request.query_params['end-date']) if "end-date" in request.query_params else single_expenses
    serializer = GetExpenseSerializer(single_expenses, many=True)
    return serializer.data


def recurring_expense_helper(request):
    multiple_expenses = RecurringExpense.objects.filter(
        user=Users.objects.get(email=request.user))
    multiple_expenses = multiple_expenses.filter(
        end_date__gte=request.query_params['start-date']) if "start-date" in request.query_params else multiple_expenses
    multiple_expenses = multiple_expenses.filter(
        start_date__lte=request.query_params['end-date']) if "end-date" in request.query_params else multiple_expenses
    single_expense_finals = []
    for j in range(0, len(multiple_expenses)):
        patch_expenses = PatchExpense.objects.filter(rec_exp=multiple_expenses[j])
        end_date_req = multiple_expenses[j].end_date
        start_date_req = multiple_expenses[j].start_date
        if "start-date" in request.query_params:
            start_date_req = datetime.strptime(request.query_params['start-date'],
                                               '%Y-%m-%d').date() if datetime.strptime(
                request.query_params['start-date'], '%Y-%m-%d').date() > multiple_expenses[j].start_date else \
                multiple_expenses[j].start_date
        if "end-date" in request.query_params:
            end_date_req = datetime.strptime(request.query_params['end-date'], '%Y-%m-%d').date() if datetime.strptime(
                request.query_params['end-date'], '%Y-%m-%d').date() < multiple_expenses[j].end_date else \
                multiple_expenses[j].end_date
        relativedelta_intermediate = relativedelta(end_date_req, start_date_req)
        time_range = end_date_req - start_date_req
        if multiple_expenses[j].unit == "d":
            for i in range(0, (time_range.days + 1)):
                patch = next((item for item in patch_expenses if item.index == i), None)
                single_expense_finals.append(
                    {"name": multiple_expenses[j].name, "value": multiple_expenses[j].value,
                     "sign": multiple_expenses[j].sign, "date": timedelta(days=i) + start_date_req, "type": "gen",
                     "id": multiple_expenses[
                         j].id}) if patch == None else single_expense_finals.append(
                    {"name": patch.name, "value": patch.value, "sign": patch.sign,
                     "date": timedelta(days=i) + start_date_req, "type": "patch", "id": patch.id})
        if multiple_expenses[j].unit == "w":
            for i in range(0, (floor(time_range.days / 7) + 1)):
                patch = next((item for item in patch_expenses if item.index == i), None)
                single_expense_finals.append(
                    {"name": multiple_expenses[j].name, "value": multiple_expenses[j].value,
                     "sign": multiple_expenses[j].sign, "date": timedelta(weeks=i) + start_date_req, "type": "gen",
                     "id": multiple_expenses[
                         j].id}) if patch == None else single_expense_finals.append(
                    {"name": patch.name, "value": patch.value, "sign": patch.sign,
                     "date": timedelta(weeks=i) + start_date_req, "type": "patch", "id": patch.id})
        if multiple_expenses[j].unit == "m":
            for i in range(0, ((relativedelta_intermediate.months +
                                relativedelta_intermediate.years * 12) + 1)):
                patch = next((item for item in patch_expenses if item.index == i), None)
                single_expense_finals.append(
                    {"name": multiple_expenses[j].name, "value": multiple_expenses[j].value,
                     "sign": multiple_expenses[j].sign, "date": relativedelta(months=i) + start_date_req, "type": "gen",
                     "id": multiple_expenses[
                         j].id}) if patch == None else single_expense_finals.append(
                    {"name": patch.name, "value": patch.value, "sign": patch.sign,
                     "date": relativedelta(months=i) + start_date_req, "type": "patch", "id": patch.id})
        if multiple_expenses[j].unit == "y":
            for i in range(0, relativedelta_intermediate.years + 1):
                patch = next((item for item in patch_expenses if item.index == i), None)
                single_expense_finals.append(
                    {"name": multiple_expenses[j].name, "value": multiple_expenses[j].value,
                     "sign": multiple_expenses[j].sign, "date": relativedelta(years=i) + start_date_req, "type": "gen",
                     "id": multiple_expenses[
                         j].id}) if patch == None else single_expense_finals.append(
                    {"name": patch.name, "value": patch.value, "sign": patch.sign,
                     "date": relativedelta(years=i) + start_date_req, "type": "patch", "id": patch.id})
    return single_expense_finals
