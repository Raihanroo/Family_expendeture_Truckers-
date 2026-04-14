"""
Family Expenditure Management System - URL Configuration
Maps URLs to views for both REST API and template-based views
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    ExpenseViewSet,
    FamilyMemberViewSet,
    IncomeSourceViewSet,
    ExpenseCategoryViewSet,
    ExpenditureViewSet,
)

# REST API Router Configuration
router = DefaultRouter()
router.register(r"expenses-api", ExpenseViewSet, basename="expense-api")
router.register(r"members", FamilyMemberViewSet, basename="member")
router.register(r"income-sources", IncomeSourceViewSet, basename="income-source")
router.register(r"categories", ExpenseCategoryViewSet, basename="category")
router.register(r"expenditures", ExpenditureViewSet, basename="expenditure")

app_name = "expenses"

urlpatterns = [
    # REST API URLs
    path("api/", include(router.urls)),
    
    # Dashboard & Home
    path("", views.home, name="home"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    
    # Expense Management
    path("add/", views.add_expense, name="add_expense"),
    path("view/", views.view_expenses, name="view_expenses"),
    path("edit/<int:pk>/", views.edit_expense, name="edit_expense"),
    path("delete/<int:pk>/", views.delete_expense, name="delete_expense"),
    path("stats/", views.expense_stats, name="stats"),
    path("expenses/export/", views.export_expenses_excel, name="export_excel"),
    
    # Budget Management
    path("budget/", views.set_budget, name="set_budget"),
    
    # Authentication
    path("register/", views.admin_register, name="register"),
    path("login/", views.login_view, name="login"),
    path("admin-login/", views.admin_login_view, name="admin_login"),
    path("user-register/", views.user_register, name="user_register"),
    path("logout/", views.logout_view, name="logout"),
    
    # Family Member Management
    path("members/add/", views.add_member, name="add_member"),
    path("members/", views.member_list, name="member_list"),
    path("members/edit/<int:pk>/", views.edit_member, name="edit_member"),
    path("members/delete/<int:pk>/", views.delete_member, name="delete_member"),
    
    # Category Management
    path("categories/manage/", views.add_category, name="add_category"),
    path("categories/edit/<int:pk>/", views.edit_category, name="edit_category"),
    path("categories/delete/<int:pk>/", views.delete_category, name="delete_category"),
    
    # User Management (Admin Only)
    path("manage-users/", views.manage_users, name="manage_users"),
    path("reset-password/<int:user_id>/", views.reset_user_password, name="reset_user_password"),
]
