import json
import os
import openpyxl
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import permissions, viewsets

from .forms import BudgetForm, ExpenseForm, FamilyMemberForm
from .models import (
    Budget,
    Expense,
    ExpenseCategory,
    Expenditure,
    FamilyMember,
    IncomeSource,
)
from .serializers import (
    ExpenseCategorySerializer,
    ExpenditureSerializer,
    ExpenseSerializer,
    FamilyMemberSerializer,
    IncomeSourceSerializer,
)


# --- API Documentation View ---
def api_docs(request):
    docs_path = os.path.join(settings.BASE_DIR, "API_Documentation.html")
    with open(docs_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HttpResponse(content, content_type="text/html")


# --- API ViewSets ---
class IncomeSourceViewSet(viewsets.ModelViewSet):
    queryset = IncomeSource.objects.all()
    serializer_class = IncomeSourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class FamilyMemberViewSet(viewsets.ModelViewSet):
    serializer_class = FamilyMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FamilyMember.objects.filter(user=self.request.user)


class ExpenditureViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenditureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expenditure.objects.filter(member__user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- Admin Dashboard ---
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin only.")
        return redirect("expenses:home")

    today = datetime.today()
    all_expenses = Expense.objects.all().select_related("category", "member__user")

    total_this_month = (
        all_expenses.filter(
            date__year=today.year, date__month=today.month
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    total_all_time = all_expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    total_expenses_count = all_expenses.count()
    expenses_this_month = all_expenses.filter(
        date__year=today.year, date__month=today.month
    ).count()

    total_members = FamilyMember.objects.count()
    admin_count = FamilyMember.objects.filter(role="ADMIN").count()
    member_count = FamilyMember.objects.filter(role="MEMBER").count()
    total_categories = ExpenseCategory.objects.count()
    total_income_sources = IncomeSource.objects.count()

    monthly_budget = Budget.objects.filter(user=request.user).first()
    budget_amount = monthly_budget.monthly_budget if monthly_budget else 0
    budget_percentage = (
        (total_this_month / budget_amount * 100) if budget_amount > 0 else 0
    )

    current_month_expenses = all_expenses.filter(
        date__year=today.year, date__month=today.month
    )
    category_breakdown = (
        current_month_expenses.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    pie_labels = [item["category__name"] or "General" for item in category_breakdown]
    pie_data = [float(item["total"]) for item in category_breakdown]

    seven_days_ago = today - timedelta(days=7)
    daily_spending = (
        all_expenses.filter(date__gte=seven_days_ago)
        .values("date")
        .annotate(total=Sum("amount"))
        .order_by("date")
    )
    bar_labels = [item["date"].strftime("%d %b") for item in daily_spending]
    bar_data = [float(item["total"]) for item in daily_spending]

    context = {
        "total_this_month": total_this_month,
        "total_all_time": total_all_time,
        "total_expenses_count": total_expenses_count,
        "expenses_this_month": expenses_this_month,
        "total_members": total_members,
        "admin_count": admin_count,
        "member_count": member_count,
        "total_categories": total_categories,
        "total_income_sources": total_income_sources,
        "monthly_budget": budget_amount,
        "budget_percentage": budget_percentage,
        "recent_expenses": all_expenses.order_by("-date")[:10],
        "pie_labels": json.dumps(pie_labels),
        "pie_data": json.dumps(pie_data),
        "bar_labels": json.dumps(bar_labels),
        "bar_data": json.dumps(bar_data),
    }
    return render(request, "expenses/admin_dashboard.html", context)


# --- Home / Dashboard ---
@login_required
def home(request):
    user = request.user
    is_admin = user.is_superuser
    search_query = request.GET.get("search", "").strip()

    if is_admin:
        all_expenses = Expense.objects.all().select_related(
            "category", "member__user", "user"
        ).order_by("-date")
    else:
        all_expenses = Expense.objects.filter(user=user).select_related(
            "category", "member__user"
        ).order_by("-date")

    converted_date = None
    if search_query:
        for fmt in ("%d %b, %Y", "%d %b %Y", "%Y-%m-%d"):
            try:
                converted_date = datetime.strptime(search_query, fmt).strftime(
                    "%Y-%m-%d"
                )
                break
            except ValueError:
                continue

        query_filter = (
            Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
            | Q(member__name__icontains=search_query)
            | Q(member__user__username__icontains=search_query)
            | Q(user__username__icontains=search_query)
        )
        if converted_date:
            query_filter |= Q(date=converted_date)
        expenses = all_expenses.filter(query_filter).distinct()
    else:
        expenses = all_expenses[:10]

    today = datetime.today()
    current_month_expenses = all_expenses.filter(
        date__year=today.year, date__month=today.month
    )
    total_this_month = (
        current_month_expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    )
    total_all_time = all_expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    category_breakdown = (
        current_month_expenses.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    pie_labels = [item["category__name"] or "General" for item in category_breakdown]
    pie_data = [float(item["total"]) for item in category_breakdown]

    seven_days_ago = today - timedelta(days=7)
    daily_spending = (
        all_expenses.filter(date__gte=seven_days_ago)
        .values("date")
        .annotate(total=Sum("amount"))
        .order_by("date")
    )
    bar_labels = [item["date"].strftime("%d %b") for item in daily_spending]
    bar_data = [float(item["total"]) for item in daily_spending]

    context = {
        "expenses": expenses,
        "total_this_month": total_this_month,
        "total_all_time": total_all_time,
        "total_expenses_count": all_expenses.count(),
        "pie_labels": json.dumps(pie_labels),
        "pie_data": json.dumps(pie_data),
        "bar_labels": json.dumps(bar_labels),
        "bar_data": json.dumps(bar_data),
        "is_admin": is_admin,
    }
    return render(request, "expenses/home.html", context)


# --- Export Excel ---
@login_required
def export_expenses_excel(request):
    search_query = request.GET.get("search", "").strip()
    expenses = Expense.objects.filter(user=request.user).select_related(
        "category", "member"
    ).order_by("-date")

    if search_query:
        query_filter = (
            Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
            | Q(member__name__icontains=search_query)
            | Q(member__user__username__icontains=search_query)
        )
        expenses = expenses.filter(query_filter).distinct()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Date", "Category", "Member", "Description", "Amount"])
    for obj in expenses:
        ws.append([
            obj.date.strftime("%d %b, %Y"),
            obj.category.name if obj.category else "General",
            obj.member.name if obj.member else "Self",
            obj.description or "",
            float(obj.amount),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="Report_{datetime.now().strftime("%Y-%m-%d")}.xlsx"'
    )
    wb.save(response)
    return response


# --- Expense CRUD ---
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect("expenses:home")
    else:
        form = ExpenseForm()
    return render(request, "expenses/add_expense.html", {"form": form})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect("expenses:home")
    else:
        form = ExpenseForm(instance=expense)
    return render(
        request, "expenses/add_expense.html", {"form": form, "edit_mode": True}
    )


@login_required
def delete_expense(request, pk):
    get_object_or_404(Expense, pk=pk, user=request.user).delete()
    messages.success(request, "Expense deleted!")
    return redirect("expenses:home")


# --- Category Management ---
@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            ExpenseCategory.objects.create(name=name)
            messages.success(request, "Category added!")
        return redirect("expenses:add_category")
    return render(
        request,
        "expenses/add_category.html",
        {"categories": ExpenseCategory.objects.all()},
    )


@login_required
def edit_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            category.name = name
            category.save()
            messages.success(request, "Category updated!")
        return redirect("expenses:add_category")
    return render(request, "expenses/edit_category.html", {"category": category})


@login_required
def delete_category(request, pk):
    get_object_or_404(ExpenseCategory, pk=pk).delete()
    return redirect("expenses:add_category")


# --- Member Management ---
@login_required
def add_member(request):
    if request.method == "POST":
        form = FamilyMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            messages.success(request, "Member added successfully!")
            return redirect("expenses:member_list")
    else:
        form = FamilyMemberForm()
    return render(
        request,
        "expenses/add_member.html",
        {"form": form, "roles": FamilyMember.ROLE_CHOICES},
    )


@login_required
def member_list(request):
    query = request.GET.get("q", "")
    members = FamilyMember.objects.filter(user=request.user)

    if query:
        members = members.filter(name__icontains=query)

    if request.GET.get("export") == "1":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Name", "Phone", "Role", "Income Source", "Salary"])
        for m in members:
            ws.append([m.name, m.phone_number, m.role, m.income_source, float(m.salary or 0)])
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=members.xlsx"
        wb.save(response)
        return response

    return render(request, "expenses/member_list.html", {"members": members})


@login_required
def edit_member(request, pk):
    member = get_object_or_404(FamilyMember, id=pk, user=request.user)
    if request.method == "POST":
        form = FamilyMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Member updated successfully!")
            return redirect("expenses:member_list")
    else:
        form = FamilyMemberForm(instance=member)
    return render(
        request,
        "expenses/add_member.html",
        {"form": form, "member": member, "edit_mode": True, "roles": FamilyMember.ROLE_CHOICES},
    )


@login_required
def delete_member(request, pk):
    get_object_or_404(FamilyMember, id=pk, user=request.user).delete()
    return redirect("expenses:member_list")


# --- Authentication ---
def register_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        e = request.POST.get("email")
        p1 = request.POST.get("password")
        p2 = request.POST.get("password_confirm")
        if p1 == p2 and not User.objects.filter(username=u).exists():
            user = User.objects.create_user(username=u, email=e, password=p1)
            user.is_staff = user.is_superuser = True
            user.save()
            return redirect("expenses:login")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect("expenses:home")
        messages.error(request, "Invalid username or password!")
        return render(request, "login.html", {"error": "Invalid username or password!"})
    return render(request, "login.html")


def admin_register(request):
    """Admin registration — limited to MAX_ADMINS superusers."""
    MAX_ADMINS = int(os.environ.get("MAX_ADMINS", 3))
    ADMIN_SECRET = os.environ.get("ADMIN_SECRET_KEY", "")

    if User.objects.filter(is_superuser=True).count() >= MAX_ADMINS:
        messages.error(request, f"Maximum admin limit ({MAX_ADMINS}) reached.")
        return redirect("expenses:login")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        secret_key = request.POST.get("secret_key", "")

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match!"})
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists!"})
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already exists!"})
        if not ADMIN_SECRET or secret_key != ADMIN_SECRET:
            return render(request, "register.html", {"error": "Invalid secret key!"})

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_superuser=True,
            is_staff=True,
        )
        messages.success(request, "Admin account created! Please login.")
        return redirect("expenses:login")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("expenses:login")


def admin_login_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(username=u, password=p)
        if user:
            if user.is_superuser:
                login(request, user)
                return redirect("expenses:admin_dashboard")
            return render(
                request,
                "login_admin.html",
                {"error": "Not an admin account! Use user login."},
            )
        return render(
            request, "login_admin.html", {"error": "Invalid username or password!"}
        )
    return render(request, "login_admin.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register_user.html", {"error": "Passwords do not match!"})
        if User.objects.filter(username=username).exists():
            return render(request, "register_user.html", {"error": "Username already exists!"})
        if User.objects.filter(email=email).exists():
            return render(request, "register_user.html", {"error": "Email already exists!"})

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_superuser=False,
            is_staff=False,
        )
        messages.success(request, "Account created successfully! Please login.")
        return redirect("expenses:login")

    return render(request, "register_user.html")


@login_required
def set_budget(request):
    budget, _ = Budget.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect("expenses:home")
    return render(
        request, "expenses/set_budget.html", {"form": BudgetForm(instance=budget)}
    )


@login_required
def view_expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    categories = ExpenseCategory.objects.all()

    category_id = request.GET.get("category")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if from_date:
        expenses = expenses.filter(date__gte=from_date)
    if to_date:
        expenses = expenses.filter(date__lte=to_date)

    if request.GET.get("export") == "1":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Date", "Category", "Description", "Amount"])
        for e in expenses:
            ws.append([
                e.date.strftime("%d %b, %Y"),
                e.category.name if e.category else "General",
                e.description or "",
                float(e.amount),
            ])
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=filtered_expenses.xlsx"
        wb.save(response)
        return response

    total_amount = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    return render(
        request,
        "expenses/view_expenses.html",
        {"expenses": expenses, "categories": categories, "total_amount": total_amount},
    )


@login_required
def expense_stats(request):
    today = datetime.today()
    monthly_expenses = Expense.objects.filter(
        user=request.user, date__year=today.year, date__month=today.month
    )
    category_summary = (
        monthly_expenses.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    context = {
        "labels": json.dumps(
            [item["category__name"] or "General" for item in category_summary]
        ),
        "data": json.dumps([float(item["total"]) for item in category_summary]),
        "category_summary": category_summary,
        "current_month": today.strftime("%B %Y"),
    }
    return render(request, "expenses/stats.html", context)
