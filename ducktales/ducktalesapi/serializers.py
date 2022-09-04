from .models import PatchExpense, SingleExpense, RecurringExpense
from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer


class InterestCalculatorRequestSerializer(serializers.Serializer):
    starting_capital = serializers.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=4, decimal_places=2)
    unit = serializers.CharField()
    duration = serializers.IntegerField(max_value=1200)
    interest_payment = serializers.BooleanField(required=False)


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=30)


class AddExpenseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    value = serializers.DecimalField(max_digits=100, decimal_places=2)
    sign = serializers.BooleanField()
    date = serializers.DateField(format='iso-8601')


class AddPatchExpenseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    value = serializers.DecimalField(max_digits=65, decimal_places=2)
    sign = serializers.BooleanField()
    id = serializers.DecimalField(max_digits=65, decimal_places=0)
    index = serializers.DecimalField(max_digits=65, decimal_places=0)


class EditPatchExpenseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    value = serializers.DecimalField(max_digits=65, decimal_places=2)
    sign = serializers.BooleanField()
    index = serializers.DecimalField(max_digits=65, decimal_places=0)


class GetExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleExpense
        fields = ['name', 'value', 'sign', 'date', 'id']


class GetPatchExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatchExpense
        fields = ['name', 'value', 'sign', 'index', 'id']


class AddRecurringExpenseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    value = serializers.DecimalField(max_digits=100, decimal_places=2)
    sign = serializers.BooleanField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    unit = serializers.CharField(max_length=1)


class GetRecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = ['name', 'value', 'sign', 'start_date', 'end_date', 'unit', 'id']


class RegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = [
            "email",
            "name",
            "surname",
            "email",
            "date_of_birth",
            "password",

        ]
