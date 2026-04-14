"""
Family Expenditure Management System - Forms
Django forms for user input validation and rendering
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, ExpenseCategory, Budget, FamilyMember


class ExpenseForm(forms.ModelForm):
    """Form for creating and editing expenses"""

    class Meta:
        model = Expense
        fields = [
            "date",
            "category",
            "member",
            "amount",
            "description",
            "is_recurring",
            "frequency",
            "recurring_end_date",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "member": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "৳ 0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Expense description",
                }
            ),
            "is_recurring": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "frequency": forms.Select(attrs={"class": "form-control"}),
            "recurring_end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False
        self.fields["category"].queryset = ExpenseCategory.objects.all()
        self.fields["category"].empty_label = "-- Select Category --"
        
        # Filter members by user
        if user:
            self.fields["member"].queryset = FamilyMember.objects.filter(user=user)
        else:
            self.fields["member"].queryset = FamilyMember.objects.all()
        
        self.fields["member"].empty_label = "-- Select Member --"
        self.fields["frequency"].required = False
        self.fields["recurring_end_date"].required = False


class UserCreationFormCustom(UserCreationForm):
    """Custom user registration form"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email address"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm password"}
        )


class BudgetForm(forms.ModelForm):
    """Form for setting monthly budget"""
    
    class Meta:
        model = Budget
        fields = ["monthly_budget"]
        widgets = {
            "monthly_budget": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter monthly budget in TK",
                    "step": "0.01",
                    "min": "0",
                }
            )
        }


class FamilyMemberForm(forms.ModelForm):
    """Form for creating and editing family members"""
    
    class Meta:
        model = FamilyMember
        fields = [
            "name",
            "father_name",
            "mother_name",
            "phone_number",
            "income_source",
            "salary",
            "address",
            "role",
            "photo",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Full name"}
            ),
            "father_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Father's name"}
            ),
            "mother_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Mother's name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone number"}
            ),
            "income_source": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Income source"}
            ),
            "salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Monthly income"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Full address",
                    "rows": 3,
                }
            ),
            "role": forms.Select(attrs={"class": "form-control"}),
        }
