"""
Family Expenditure Management System - Serializers
Converts database models to JSON format for REST API
"""
from rest_framework import serializers
from .models import FamilyMember, IncomeSource, ExpenseCategory, Expenditure, Expense


class IncomeSourceSerializer(serializers.ModelSerializer):
    """Serializer for IncomeSource model"""
    
    class Meta:
        model = IncomeSource
        fields = "__all__"


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """Serializer for ExpenseCategory model"""
    
    class Meta:
        model = ExpenseCategory
        fields = "__all__"


class FamilyMemberSerializer(serializers.ModelSerializer):
    """Serializer for FamilyMember model with all fields"""
    
    class Meta:
        model = FamilyMember
        fields = [
            "id",
            "user",
            "role",
            "joined_date",
            "name",
            "father_name",
            "mother_name",
            "phone_number",
            "address",
            "income_source",
            "salary",
        ]


class ExpenditureSerializer(serializers.ModelSerializer):
    """Serializer for Expenditure model with related field names"""
    
    member_name = serializers.CharField(source="member.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expenditure
        fields = [
            "id",
            "member",
            "member_name",
            "category",
            "category_name",
            "amount",
            "description",
            "date",
            "created_at",
        ]


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model"""
    
    class Meta:
        model = Expense
        fields = "__all__"
