# Family Expenditure Management System - API Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Data Models](#data-models)
3. [REST API Endpoints (Django REST Framework)](#rest-api-endpoints)
4. [Template-Based Views](#template-based-views)
5. [Authentication & Authorization](#authentication--authorization)
6. [How Each API Works](#how-each-api-works)

---

## 1. Project Overview

This is a **Family Expenditure Management System** built with Django and Django REST Framework. It allows families to track expenses, manage budgets, and monitor spending patterns. The project supports both regular users and admin users with different access levels.

**Technology Stack:**
- Django 4.x (Web Framework)
- Django REST Framework (API)
- SQLite/PostgreSQL (Database)
- XLWT & OpenPyXL (Excel Export)
- Cloudinary (Image Storage)

---

## 2. Data Models

### 2.1 Expense Model
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Unique identifier |
| `user` | ForeignKey (User) | Owner of the expense |
| `amount` | DecimalField | Expense amount (max 10 digits, 2 decimal places) |
| `category` | ForeignKey (ExpenseCategory) | Expense category (optional) |
| `member` | ForeignKey (FamilyMember) | Family member who made the expense |
| `description` | TextField | Description of expense |
| `date` | DateField | Date of expense |
| `created_at` | DateTimeField | When record was created |
| `updated_at` | DateTimeField | Last update time |
| `is_recurring` | BooleanField | Whether expense repeats |
| `frequency` | CharField | ONCE/DAILY/WEEKLY/MONTHLY/YEARLY |
| `recurring_end_date` | DateField | End date for recurring expenses |

### 2.2 Budget Model
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Unique identifier |
| `user` | OneToOneField (User) | User's budget (one per user) |
| `monthly_budget` | DecimalField | Monthly budget limit |
| `alert_percentage` | IntegerField | Alert threshold (default 80%) |
| `created_at` | DateTimeField | Creation timestamp |
| `updated_at` | DateTimeField | Last update timestamp |

### 2.3 FamilyMember Model
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Unique identifier |
| `user` | ForeignKey (User) | Associated Django user |
| `photo` | CloudinaryField | Member photo |
| `role` | CharField | ADMIN/MEMBER/VISITOR |
| `joined_date` | DateTimeField | When joined |
| `name` | CharField | Member name |
| `father_name` | CharField | Father's name |
| `mother_name` | CharField | Mother's name |
| `phone_number` | CharField | Contact number |
| `address` | TextField | Address |
| `income_source` | CharField | Source of income |
| `salary` | DecimalField | Monthly salary/income |

### 2.4 ExpenseCategory Model
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Unique identifier |
| `name` | CharField | Category name |

### 2.5 IncomeSource Model
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Unique identifier |
| `name` | CharField | Income source name |

### 2.6 Expenditure Model
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Unique identifier |
| `member` | ForeignKey (FamilyMember) | Who spent |
| `category` | ForeignKey (ExpenseCategory) | Category of expense |
| `amount` | DecimalField | Amount spent |
| `description` | TextField | Description |
| `date` | DateField | Date of expenditure |
| `created_at` | DateTimeField | Creation timestamp |

---

## 3. REST API Endpoints (Django REST Framework)

The project uses Django REST Framework's `ModelViewSet` to provide full CRUD (Create, Read, Update, Delete) REST APIs.

### 3.1 API Base URL
```
http://yourdomain.com/api/
```

### 3.2 All REST API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|-----------------|
| `/api/expenses-api/` | GET, POST | List/Create expenses | Required |
| `/api/expenses-api/{id}/` | GET, PUT, PATCH, DELETE | Retrieve/Update/Delete expense | Required |
| `/api/members/` | GET, POST | List/Create family members | Required |
| `/api/members/{id}/` | GET, PUT, PATCH, DELETE | Retrieve/Update/Delete member | Required |
| `/api/income-sources/` | GET, POST | List/Create income sources | Required |
| `/api/income-sources/{id}/` | GET, PUT, PATCH, DELETE | Retrieve/Update/Delete income source | Required |
| `/api/categories/` | GET, POST | List/Create expense categories | Required |
| `/api/categories/{id}/` | GET, PUT, PATCH, DELETE | Retrieve/Update/Delete category | Required |
| `/api/expenditures/` | GET, POST | List/Create expenditures | Required |
| `/api/expenditures/{id}/` | GET, PUT, PATCH, DELETE | Retrieve/Update/Delete expenditure | Required |

### 3.3 API Details

#### A) Expense API (`/api/expenses-api/`)
**ViewSet:** `ExpenseViewSet`

- **GET /api/expenses-api/** - List all expenses for the authenticated user
- **POST /api/expenses-api/** - Create a new expense
- **GET /api/expenses-api/{id}/** - Get a specific expense
- **PUT /api/expenses-api/{id}/** - Update an expense (full update)
- **PATCH /api/expenses-api/{id}/** - Partial update
- **DELETE /api/expenses-api/{id}/** - Delete an expense

**Serializer:** `ExpenseSerializer`
**Fields:** All fields from Expense model

**Special Logic:** The `get_queryset` method filters expenses by `user=request.user`, so users only see their own expenses.

---

#### B) Family Member API (`/api/members/`)
**ViewSet:** `FamilyMemberViewSet`

- **GET /api/members/** - List all family members
- **POST /api/members/** - Create a new family member
- **GET /api/members/{id}/** - Get member details
- **PUT /api/members/{id}/** - Update member
- **DELETE /api/members/{id}/** - Delete member

**Serializer:** `FamilyMemberSerializer`

**Fields:**
```json
{
    "id": 1,
    "user": 1,
    "role": "MEMBER",
    "joined_date": "2024-01-01T00:00:00Z",
    "name": "John Doe",
    "father_name": "Mr. Smith",
    "mother_name": "Mrs. Smith",
    "phone_number": "1234567890",
    "address": "123 Main St",
    "income_source": "Job",
    "income_source_name": "Job (read-only)",
    "salary": 50000.00
}
```

---

#### C) Income Source API (`/api/income-sources/`)
**ViewSet:** `IncomeSourceViewSet`

- **GET /api/income-sources/** - List all income sources
- **POST /api/income-sources/** - Create income source
- **GET /api/income-sources/{id}/** - Get income source
- **PUT /api/income-sources/{id}/** - Update income source
- **DELETE /api/income-sources/{id}/** - Delete income source

**Serializer:** `IncomeSourceSerializer`

**Fields:**
```json
{
    "id": 1,
    "name": "Salary"
}
```

---

#### D) Expense Category API (`/api/categories/`)
**ViewSet:** `ExpenseCategoryViewSet`

- **GET /api/categories/** - List all categories
- **POST /api/categories/** - Create category
- **GET /api/categories/{id}/** - Get category
- **PUT /api/categories/{id}/** - Update category
- **DELETE /api/categories/{id}/** - Delete category

**Serializer:** `ExpenseCategorySerializer`

**Fields:**
```json
{
    "id": 1,
    "name": "Food"
}
```

---

#### E) Expenditure API (`/api/expenditures/`)
**ViewSet:** `ExpenditureViewSet`

- **GET /api/expenditures/** - List all expenditures
- **POST /api/expenditures/** - Create expenditure
- **GET /api/expenditures/{id}/** - Get expenditure
- **PUT /api/expenditures/{id}/** - Update expenditure
- **DELETE /api/expenditures/{id}/** - Delete expenditure

**Serializer:** `ExpenditureSerializer`

**Fields:**
```json
{
    "id": 1,
    "member": 1,
    "member_name": "John Doe",
    "category": 1,
    "category_name": "Food",
    "amount": 500.00,
    "description": "Lunch",
    "date": "2024-01-15",
    "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 4. Template-Based Views

These are traditional Django views that render HTML templates.

### 4.1 All Template View URLs

| URL Pattern | View Name | Description |
|-------------|-----------|-------------|
| `/` | `home` | Main dashboard |
| `/admin-dashboard/` | `admin_dashboard` | Admin-only dashboard |
| `/add/` | `add_expense` | Add new expense |
| `/view/` | `view_expenses` | View all expenses with filters |
| `/edit/<int:pk>/` | `edit_expense` | Edit specific expense |
| `/delete/<int:pk>/` | `delete_expense` | Delete specific expense |
| `/stats/` | `expense_stats` | Expense statistics |
| `/budget/` | `set_budget` | Set monthly budget |
| `/register/` | `register_view` OR `admin_register` | User registration |
| `/login/` | `login_view` | User login |
| `/admin-login/` | `admin_login_view` | Admin login |
| `/user-register/` | `user_register` | Regular user registration |
| `/logout/` | `logout_view` | Logout |
| `/members/add/` | `add_member` | Add family member |
| `/members/` | `member_list` | List all members |
| `/members/edit/<int:pk>/` | `edit_member` | Edit member |
| `/members/delete/<int:pk>/` | `delete_member` | Delete member |
| `/categories/manage/` | `add_category` | Manage categories |
| `/categories/edit/<int:pk>/` | `edit_category` | Edit category |
| `/categories/delete/<int:pk>/` | `delete_category` | Delete category |
| `/expenses/export/` | `export_expenses_excel` | Export to Excel |

---

## 5. Authentication & Authorization

### 5.1 Authentication Methods
- **Session Authentication** - Used by template views
- **Token Authentication** - Can be added for API access

### 5.2 User Roles

| Role | Description | Access Level |
|------|-------------|--------------|
| **Superuser/Admin** | Django superuser (`is_superuser=True`) | Can see all expenses, access admin dashboard |
| **Regular User** | Normal Django user | Can only see their own expenses |
| **Family Member** | Added via `FamilyMember` model | Can be assigned ADMIN/MEMBER/VISITOR roles |

### 5.3 Permission Classes (REST API)
All REST API ViewSets use `permissions.IsAuthenticated`:
- Only authenticated users can access APIs
- Each user can only see their own data (filtered in `get_queryset`)

---

## 6. How Each API Works

### 6.1 Expense Management Flow

#### Adding an Expense (Template)
1. User visits `/add/` (calls `add_expense` view)
2. Form displayed with fields: amount, category, member, description, date, is_recurring, frequency
3. User submits form via POST
4. `ExpenseForm` validates data
5. `expense.user = request.user` assigns ownership
6. Expense saved to database
7. Redirect to `home` with success message

#### Editing an Expense
1. User visits `/edit/<pk>/` (calls `edit_expense` view)
2. Existing expense fetched via `get_object_or_404(Expense, pk=pk, user=request.user)`
3. Form pre-filled with existing data
4. User modifies and submits
5. Form saves changes and redirects

#### Deleting an Expense
1. User visits `/delete/<pk>/` (calls `delete_expense` view)
2. Expense fetched and deleted in one step
3. Redirect to `home` with success message

---

### 6.2 Family Member Management

#### Adding a Member
1. User visits `/members/add/` (calls `add_member` view)
2. `FamilyMemberForm` displayed with fields: name, photo, role, phone, address, income_source, salary
3. On POST: `form.save(commit=False)` → assign `member.user = request.user` → save
4. Redirect to `member_list`

#### Editing/Deleting Member
- `/members/edit/<pk>/` - Edit existing member
- `/members/delete/<pk>/` - Delete member (only if owned by current user)

#### Member Export to Excel
1. User visits `/members/?export=1`
2. All members filtered by `user=request.user`
3. OpenPyXL creates Excel file with columns: Name, Phone, Role, Income Source, Salary
4. File returned as download with MIME type `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

---

### 6.3 Category Management

#### Adding Category
1. User visits `/categories/manage/` (calls `add_category` view)
2. Simple form with only "name" field
3. On POST: `ExpenseCategory.objects.create(name=name)`
4. Redirects back to same page with updated list

#### Editing Category
1. `/categories/edit/<pk>/` - Shows edit form
2. On POST: Updates name and saves

#### Deleting Category
1. `/categories/delete/<pk>/` - Deletes category directly

---

### 6.4 Budget Management

#### Setting Budget
1. User visits `/budget/` (calls `set_budget` view)
2. `Budget.objects.get_or_create(user=request.user)` - Gets existing or creates new
3. Form allows setting: monthly_budget, alert_percentage
4. On POST: Form saves and redirects to home

---

### 6.5 Expense Filtering & Export

#### Viewing Expenses with Filters
1. User visits `/view/` (calls `view_expenses` view)
2. URL parameters: `?category=1&from_date=2024-01-01&to_date=2024-01-31`
3. Filter logic:
   - `category_id` → filters by category
   - `from_date` → filters `date__gte=from_date`
   - `to_date` → filters `date__lte=to_date`
4. Total calculated via `expenses.aggregate(Sum("amount"))`

#### Exporting to Excel
1. User visits `/view/?export=1` or `/expenses/export/`
2. OpenPyXL creates workbook
3. Adds headers: Date, Category, Description, Amount
4. Returns as downloadable `.xlsx` file

---

### 6.6 Dashboard & Statistics

#### Home Dashboard (`/`)
1. Fetches expenses filtered by user (or all if admin)
2. Calculates statistics:
   - Total this month: Sum of expenses in current month
   - Total all time: Sum of all expenses
   - Category breakdown: Groups by category with totals
3. Prepares chart data:
   - Pie chart: Category-wise spending
   - Bar chart: Last 7 days daily spending
4. Search functionality: Searches description, category name, member name, username

#### Admin Dashboard (`/admin-dashboard/`)
1. Only accessible to superusers (`is_superuser=True`)
2. Shows ALL expenses from ALL users
3. Additional stats:
   - Total members count
   - Admin vs member count
   - Categories count
   - Income sources count
   - Budget percentage used

#### Statistics Page (`/stats/`)
1. Shows current month expenses by category
2. Groups by category with totals
3. Prepares JSON data for charts

---

### 6.7 Authentication Flow

#### User Registration
1. User visits `/register/` or `/user-register/`
2. Form fields: username, email, password, confirm_password
3. For admin registration: additional `secret_key` field (default: "admin123")
4. Validation checks:
   - Passwords match
   - Username not exists
   - Email not exists
   - Secret key correct (for admin)
5. Creates User with:
   - Admin: `is_superuser=True`, `is_staff=True`
   - Regular user: `is_superuser=False`, `is_staff=False`
6. Redirects to login

#### Login
1. User visits `/login/`
2. Submits username and password
3. `authenticate(username=u, password=p)` checks credentials
4. On success: `login(request, user)` creates session
5. Redirects to home

#### Admin Login
1. User visits `/admin-login/`
2. Same authentication process
3. Additional check: `user.is_superuser` must be True
4. Redirects to admin_dashboard

#### Logout
1. User visits `/logout/`
2. `logout(request)` clears session
3. Redirects to login

---

### 6.8 REST API Workflow

#### Using the REST API

**1. Get All Expenses:**
```http
GET /api/expenses-api/
Authorization: Session or Token
```

Response:
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "amount": "500.00",
            "category": 1,
            "member": 1,
            "description": "Groceries",
            "date": "2024-01-15",
            "is_recurring": false,
            "frequency": null
        }
    ]
}
```

**2. Create New Expense:**
```http
POST /api/expenses-api/
Content-Type: application/json
Authorization: Session or Token

{
    "amount": "500.00",
    "category": 1,
    "member": 1,
    "description": "Groceries",
    "date": "2024-01-15"
}
```

**3. Update Expense:**
```http
PUT /api/expenses-api/1/
Content-Type: application/json
Authorization: Session or Token

{
    "amount": "750.00",
    "category": 1,
    "member": 1,
    "description": "Updated Groceries",
    "date": "2024-01-15"
}
```

**4. Delete Expense:**
```http
DELETE /api/expenses-api/1/
Authorization: Session or Token
```

---

## 7. Quick Reference

### URL Summary Table

| Endpoint | Type | Method | Auth | Description |
|----------|------|--------|------|-------------|
| `/api/expenses-api/` | REST | GET/POST | Yes | Expense CRUD |
| `/api/members/` | REST | GET/POST | Yes | Member CRUD |
| `/api/income-sources/` | REST | GET/POST | Yes | Income Source CRUD |
| `/api/categories/` | REST | GET/POST | Yes | Category CRUD |
| `/api/expenditures/` | REST | GET/POST | Yes | Expenditure CRUD |
| `/` | Template | GET | Yes | Home Dashboard |
| `/admin-dashboard/` | Template | GET | Yes (Admin) | Admin Dashboard |
| `/add/` | Template | GET/POST | Yes | Add Expense |
| `/view/` | Template | GET | Yes | View Expenses |
| `/edit/<pk>/` | Template | GET/POST | Yes | Edit Expense |
| `/delete/<pk>/` | Template | GET | Yes | Delete Expense |
| `/stats/` | Template | GET | Yes | Statistics |
| `/budget/` | Template | GET/POST | Yes | Set Budget |
| `/login/` | Template | GET/POST | No | User Login |
| `/admin-login/` | Template | GET/POST | No | Admin Login |
| `/register/` | Template | GET/POST | No | Registration |
| `/logout/` | Template | GET | Yes | Logout |
| `/members/add/` | Template | GET/POST | Yes | Add Member |
| `/members/` | Template | GET | Yes | Member List |
| `/members/edit/<pk>/` | Template | GET/POST | Yes | Edit Member |
| `/members/delete/<pk>/` | Template | GET | Yes | Delete Member |
| `/categories/manage/` | Template | GET/POST | Yes | Manage Categories |
| `/expenses/export/` | Template | GET | Yes | Export Excel |

---

## 8. How to Use APIs

### For Web/Templates:
1. Open browser and navigate to the URL
2. Login if required
3. Forms will be displayed for data entry
4. Data is processed and displayed in HTML

### For Mobile/External Apps:
1. Use REST API endpoints
2. Include session cookie or authentication token
3. Send JSON requests for Create/Update
4. Receive JSON responses

### For Testing (using curl):
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -d "username=admin&password=admin123"

# Get expenses
curl http://localhost:8000/api/expenses-api/ \
  -b "sessionid=YOUR_SESSION_ID"

# Create expense
curl -X POST http://localhost:8000/api/expenses-api/ \
  -b "sessionid=YOUR_SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"amount": "500", "category": 1, "date": "2024-01-15"}'
```

---

**Document Generated:** Family Expenditure Management System API Documentation
**Project Location:** `c:/Users/HP/Desktop/Family_expendeture`
