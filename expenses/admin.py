from django.contrib import admin
from .models import (
    ExpenseCategory,
    FamilyMember,
    Expenditure,
    Budget,
    SavingsGoal,
    ActivityLog,
    IncomeSource,
    Expense,
)


# Expense Admin - with full customization
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "category",
        "amount",
        "member",
        "date",
        "is_recurring",
        "frequency",
    ]
    list_filter = ["category", "date", "is_recurring", "frequency", "created_at"]
    search_fields = ["user__username", "description", "category__name"]
    date_hierarchy = "date"
    ordering = ["-date"]
    list_per_page = 50


# ExpenseCategory Admin
@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


# FamilyMember Admin
@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "role", "phone_number", "joined_date"]
    list_filter = ["role", "joined_date"]
    search_fields = ["name", "user__username", "phone_number"]
    list_per_page = 30


# Expenditure Admin
@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ["member", "category", "amount", "date", "created_at"]
    list_filter = ["category", "date", "created_at"]
    search_fields = ["member__name", "description", "category__name"]
    date_hierarchy = "date"
    ordering = ["-date"]
    list_per_page = 50


# Budget Admin
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["user", "monthly_budget", "alert_percentage", "created_at"]
    search_fields = ["user__username"]


# SavingsGoal Admin
@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "goal_name",
        "target_amount",
        "current_amount",
        "deadline",
        "get_percentage",
    ]
    list_filter = ["deadline"]
    search_fields = ["user__username", "goal_name"]
    ordering = ["-deadline"]


# ActivityLog Admin
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "model_name", "timestamp"]
    list_filter = ["model_name", "timestamp"]
    search_fields = ["user__username", "action", "details"]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]
    list_per_page = 50


# IncomeSource Admin
@admin.register(IncomeSource)
class IncomeSourceAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
