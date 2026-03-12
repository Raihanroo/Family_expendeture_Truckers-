from django.contrib import admin
from django.contrib.admin import AdminSite
from django import forms
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


# Custom Admin Site with CSS
class CustomAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        return urls

    def each_context(self, request):
        context = super().each_context(request)
        return context


# Create custom admin site instance
custom_admin_site = CustomAdminSite(name="custom_admin")


# Custom Admin - with full customization and beautiful CSS
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

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


# ExpenseCategory Admin
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


# FamilyMember Admin
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "role",
        "phone_number",
        "salary",
        "total_expenditure",
        "total_expenses_count",
        "joined_date",
    ]
    list_filter = ["role", "joined_date"]
    search_fields = ["name", "user__username", "phone_number"]
    list_per_page = 30
    readonly_fields = ["total_expenditure", "total_expenses_count"]

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


# Expenditure Admin
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ["member", "category", "amount", "date", "created_at"]
    list_filter = ["category", "date", "created_at"]
    search_fields = ["member__name", "description", "category__name"]
    date_hierarchy = "date"
    ordering = ["-date"]
    list_per_page = 50

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


# Budget Admin
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["user", "monthly_budget", "alert_percentage", "created_at"]
    search_fields = ["user__username"]

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


# SavingsGoal Admin
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

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


# ActivityLog Admin
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "model_name", "timestamp"]
    list_filter = ["model_name", "timestamp"]
    search_fields = ["user__username", "action", "details"]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]
    list_per_page = 50

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


# IncomeSource Admin
class IncomeSourceAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


# Register all models with custom admin classes
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(Expenditure, ExpenditureAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(SavingsGoal, SavingsGoalAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(IncomeSource, IncomeSourceAdmin)
