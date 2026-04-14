# Family Expenditure Management System

A comprehensive Django-based web application for tracking family expenses, managing budgets, and monitoring spending patterns. Built with Django REST Framework for API support and modern web technologies.

## 🎯 Project Overview

This system allows families to:
- Track daily expenses with categories
- Manage family members and their spending
- Set and monitor monthly budgets
- Generate expense reports and statistics
- Export data to Excel
- Access data via REST API
- Admin can manage users and reset passwords

## 🚀 Features

### Core Features
- **User Authentication**: Secure login system with admin and regular user roles
- **Expense Tracking**: Add, edit, delete, and view expenses with detailed information
- **Category Management**: Organize expenses by customizable categories
- **Family Member Management**: Track which family member made each expense
- **Budget Management**: Set monthly budgets with alert thresholds
- **User Management**: Admin can view all users and reset passwords
- **Search & Filter**: Find expenses by date, category, member, user, or description
- **Data Export**: Export expenses and member data to Excel
- **Statistics Dashboard**: Visual charts showing spending patterns
- **REST API**: Full CRUD API for mobile/external app integration

### User Roles
- **Admin**: Full access to all expenses, member management, user management, and system settings
- **Regular User**: Access to personal expenses and family member data

### Admin Features
- View all users' expenses with user filter
- Manage all family members across users
- Reset passwords for any user (admin or regular)
- Access comprehensive dashboard with system-wide statistics
- Export all data with user information

### Regular User Features
- View only personal expenses
- Manage own family members
- Set personal budget
- Export personal data
- View personal statistics

## 📋 Technology Stack

### Backend
- **Django 5.2.10**: Web framework
- **Django REST Framework 3.16.1**: API development
- **SQLite**: Database (production-ready)
- **Python 3.x**: Programming language

### Frontend
- **HTML5/CSS3**: Structure and styling
- **Bootstrap 5**: UI framework (via crispy-bootstrap5)
- **JavaScript**: Interactive features
- **Chart.js 3.9.1**: Data visualization
- **Font Awesome 6.4.0**: Icons

### Storage & Deployment
- **Cloudinary**: Image storage for member photos
- **WhiteNoise**: Static file serving
- **Gunicorn**: WSGI HTTP server

### Additional Libraries
- **openpyxl**: Excel file generation
- **python-dotenv**: Environment variable management
- **Pillow**: Image processing
- **dj-database-url**: Database configuration

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Family_expenditure
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ADMIN_SECRET_KEY=your-admin-secret
MAX_ADMINS=3
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-key
CLOUDINARY_API_SECRET=your-cloudinary-secret
```

### Step 5: Database Setup
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## 📁 Project Structure

```
Family_expenditure/
├── core/                      # Project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── expenses/                  # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── urls.py               # App URL patterns
│   ├── forms.py              # Django forms
│   ├── serializers.py        # DRF serializers
│   ├── admin.py              # Admin configuration
│   ├── templates/            # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Admin registration
│   │   ├── register_user.html # User registration
│   │   └── expenses/        # Expense templates
│   │       ├── home.html    # User dashboard
│   │       ├── admin_dashboard.html # Admin dashboard
│   │       ├── add_expense.html
│   │       ├── view_expenses.html
│   │       ├── manage_users.html # User management
│   │       ├── reset_password.html # Password reset
│   │       ├── member_list.html
│   │       ├── add_member.html
│   │       ├── add_category.html
│   │       ├── set_budget.html
│   │       └── stats.html
│   └── migrations/           # Database migrations
├── static/                    # Static files (CSS, JS)
│   └── admin/                # Admin static files
├── media/                     # User uploads
│   └── member_photos/        # Member profile photos
├── staticfiles/              # Collected static files
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── .env                      # Environment variables
├── .gitignore               # Git ignore file
├── COMPLETE_PROJECT_DOCUMENTATION.md # Full documentation
└── Readme.md                 # This file
```

## 🔐 User Guide

### Registration & Login

#### Regular User Registration
1. Visit `/expenses/user-register/`
2. Fill in username, email, and password
3. Click "Register"
4. Login at `/expenses/login/`

#### Admin Registration
1. Visit `/expenses/register/`
2. Provide username, email, password, and admin secret key
3. Limited to MAX_ADMINS (default: 3)
4. Login at `/expenses/admin-login/`

### Default Admin Credentials
- **Username**: raihan12
- **Password**: admin123

### Managing Expenses

#### Add Expense
1. Login to your account
2. Click "Add New Expenditure"
3. Fill in:
   - Date
   - Category
   - Family Member (your own members only)
   - Amount
   - Description
   - Recurring options (if applicable)
4. Click "Save"

#### View Expenses
- **Regular User**: See only personal expenses
- **Admin**: See all expenses with user filter option

#### Edit/Delete Expense
- Click "Edit" button on any expense
- Modify fields and save
- Click "Delete" to remove (confirmation required)

### Managing Categories
1. Navigate to "Manage Categories"
2. Add new categories or edit existing ones
3. Categories are shared across all users
4. Admin can manage all categories

### Managing Family Members
1. Go to "Members" section
2. Click "Add Member"
3. Fill in member details:
   - Name, photo, contact info
   - Income source and salary
   - Role (Admin/Member/Visitor)
4. Each user sees only their own members
5. Admin can see all members

### User Management (Admin Only)
1. Login as admin
2. Go to Admin Dashboard
3. Click "User Management" card or "Manage Users" in sidebar
4. View all users (admin and regular)
5. Click "Reset Password" on any user
6. Enter new password twice and submit

### Password Reset
- Regular users: Contact admin to reset password
- Admin: Can reset any user's password from "Manage Users" page

### Setting Budget
1. Navigate to "Set Budget"
2. Enter monthly budget amount
3. Set alert percentage (default: 80%)
4. System will warn when spending exceeds threshold

### Viewing Statistics
- **User Dashboard**: Shows personal statistics
  - Total spending (this month & all time)
  - Category breakdown (pie chart)
  - Daily spending trend (bar chart)
  - Recent expenses list

- **Admin Dashboard**: Shows system-wide statistics
  - All users' total spending
  - Total transactions
  - Total members
  - Category breakdown
  - Time-based spending trends (7 days, 30 days, 3 months, 6 months, year)

### Exporting Data
- **Expenses**: Click "Export" on view expenses page
  - Regular user: Exports personal expenses
  - Admin: Exports all expenses with user column
- **Members**: Click "Export" on member list page
- Downloads as Excel (.xlsx) file

## 🌐 API Documentation

### Base URL
```
http://localhost:8000/expenses/api/
```

### Authentication
All API endpoints require authentication (Session or Token).

### Endpoints

#### Expenses API
- `GET /expenses/api/expenses-api/` - List all expenses
- `POST /expenses/api/expenses-api/` - Create expense
- `GET /expenses/api/expenses-api/{id}/` - Get expense details
- `PUT /expenses/api/expenses-api/{id}/` - Update expense
- `PATCH /expenses/api/expenses-api/{id}/` - Partial update
- `DELETE /expenses/api/expenses-api/{id}/` - Delete expense

#### Family Members API
- `GET /expenses/api/members/` - List members
- `POST /expenses/api/members/` - Create member
- `GET /expenses/api/members/{id}/` - Get member
- `PUT /expenses/api/members/{id}/` - Update member
- `PATCH /expenses/api/members/{id}/` - Partial update
- `DELETE /expenses/api/members/{id}/` - Delete member

#### Categories API
- `GET /expenses/api/categories/` - List categories
- `POST /expenses/api/categories/` - Create category
- `GET /expenses/api/categories/{id}/` - Get category
- `PUT /expenses/api/categories/{id}/` - Update category
- `PATCH /expenses/api/categories/{id}/` - Partial update
- `DELETE /expenses/api/categories/{id}/` - Delete category

#### Income Sources API
- `GET /expenses/api/income-sources/` - List income sources
- `POST /expenses/api/income-sources/` - Create income source
- `GET /expenses/api/income-sources/{id}/` - Get income source
- `PUT /expenses/api/income-sources/{id}/` - Update income source
- `DELETE /expenses/api/income-sources/{id}/` - Delete income source

#### Expenditures API
- `GET /expenses/api/expenditures/` - List expenditures
- `POST /expenses/api/expenditures/` - Create expenditure
- `GET /expenses/api/expenditures/{id}/` - Get expenditure
- `PUT /expenses/api/expenditures/{id}/` - Update expenditure
- `DELETE /expenses/api/expenditures/{id}/` - Delete expenditure

### Example API Requests

#### Get All Expenses
```bash
curl -X GET http://localhost:8000/expenses/api/expenses-api/ \
  -H "Authorization: Token your-token-here"
```

#### Create Expense
```bash
curl -X POST http://localhost:8000/expenses/api/expenses-api/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{
    "amount": "500.00",
    "category": 1,
    "date": "2026-01-15",
    "description": "Groceries"
  }'
```

#### Update Expense
```bash
curl -X PUT http://localhost:8000/expenses/api/expenses-api/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{
    "amount": "600.00",
    "category": 1,
    "date": "2026-01-15",
    "description": "Groceries - Updated"
  }'
```

#### Delete Expense
```bash
curl -X DELETE http://localhost:8000/expenses/api/expenses-api/1/ \
  -H "Authorization: Token your-token-here"
```

#### Create Family Member
```bash
curl -X POST http://localhost:8000/expenses/api/members/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{
    "name": "John Doe",
    "role": "Member",
    "phone": "01712345678",
    "salary": "50000.00"
  }'
```

### API Response Format

#### Success Response
```json
{
  "id": 1,
  "amount": "500.00",
  "category": {
    "id": 1,
    "name": "Food"
  },
  "date": "2026-01-15",
  "description": "Groceries",
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T10:30:00Z"
}
```

#### Error Response
```json
{
  "detail": "Authentication credentials were not provided."
}
```

## 🔒 Security Features

- **Password Encryption**: All passwords stored with Django's built-in PBKDF2 hashing
- **CSRF Protection**: Forms protected against cross-site request forgery
- **Session Management**: Secure session handling with 2-week expiry
- **User Isolation**: Regular users can only access their own data
- **Admin Restrictions**: Admin features require superuser status
- **Environment Variables**: Sensitive data stored in .env file
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping enabled
- **Password Reset**: Secure password reset by admin only

## 📊 Database Models

### User (Django Built-in)
- Username, Email, Password
- is_superuser, is_staff, is_active
- date_joined, last_login

### Expense
- user (ForeignKey to User)
- amount (DecimalField)
- category (ForeignKey to ExpenseCategory)
- member (ForeignKey to FamilyMember, optional)
- description (TextField)
- date (DateField)
- is_recurring (BooleanField)
- recurring_frequency (CharField)
- recurring_end_date (DateField, optional)
- created_at, updated_at (DateTimeField)

### FamilyMember
- user (ForeignKey to User)
- name (CharField)
- photo (ImageField, optional)
- role (CharField: Admin/Member/Visitor)
- phone (CharField, optional)
- address (TextField, optional)
- income_source (ForeignKey to IncomeSource, optional)
- salary (DecimalField, optional)
- created_at, updated_at (DateTimeField)

### ExpenseCategory
- name (CharField, unique)

### Budget
- user (OneToOneField to User)
- monthly_budget (DecimalField)
- alert_percentage (IntegerField, default=80)

### IncomeSource
- name (CharField, unique)

### Expenditure
- member (ForeignKey to FamilyMember)
- category (ForeignKey to ExpenseCategory)
- amount (DecimalField)
- description (TextField)
- date (DateField)

## 🎨 UI Features

### Responsive Design
- Mobile-friendly interface
- Adaptive layouts for all screen sizes
- Touch-optimized controls

### Modern UI Components
- Gradient backgrounds
- Card-based layouts
- Interactive charts (Chart.js)
- Icon integration (Font Awesome)
- Smooth animations and transitions

### Dashboard Features
- Real-time statistics
- Visual data representation
- Quick action buttons
- Recent activity feed

## 🐛 Troubleshooting

### Server won't start
```bash
python manage.py runserver
```

### Port 8000 in use
```bash
python manage.py runserver 8001
```

### Database errors
```bash
python manage.py migrate
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Can't login
- Verify username and password
- Check if user exists in database
- Ensure migrations are applied

### Forgot password
- Contact admin to reset password
- Admin can reset from "Manage Users" page

### Member dropdown empty
- Ensure you have added family members
- Check if members belong to your user account

## 📝 Development Notes

### Adding New Features
1. Create models in `expenses/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Create views in `expenses/views.py`
5. Add URL patterns in `expenses/urls.py`
6. Create templates in `expenses/templates/`
7. Update serializers for API support

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions small and focused

### Testing
```bash
python manage.py test
```

## 🎓 Learning Outcomes

This project demonstrates:
- **Django Framework**: Models, Views, Templates, Forms
- **REST API Development**: Django REST Framework, Serializers
- **Database Design**: Relational database modeling, ORM
- **User Authentication**: Login, Registration, Permissions
- **Authorization**: Role-based access control
- **File Handling**: Image uploads, Cloudinary integration
- **Data Visualization**: Chart.js integration
- **Excel Export**: openpyxl library usage
- **Frontend Development**: HTML, CSS, JavaScript, Bootstrap
- **Security**: CSRF, XSS, SQL injection prevention
- **Deployment**: Static files, Media files, Production settings

## 📈 Project Statistics

- **Total Lines of Code**: 5000+
- **Models**: 6
- **Views**: 25+
- **Templates**: 15+
- **API Endpoints**: 25+
- **Development Time**: 3+ months
- **Features Implemented**: 20+

## 🤝 Contributing

This is an academic project. For educational purposes only.

## 📄 License

This project is for educational purposes.

## 👥 Contact

For questions or support, please contact the project maintainer.

---

**Version**: 2.0.0  
**Last Updated**: April 2026  
**Django Version**: 5.2.10  
**Python Version**: 3.8+  
**Status**: Production Ready
