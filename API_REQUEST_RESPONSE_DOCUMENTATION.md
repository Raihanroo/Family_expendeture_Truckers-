# Family Expenditure Management System
## Complete API Request & Response Documentation

**Base URL:** `http://localhost:8000/expenses/api/`

**Authentication:** Required for all endpoints (Session-based)

---

## Table of Contents

1. [Expenses API](#expenses-api)
2. [Family Members API](#family-members-api)
3. [Categories API](#categories-api)
4. [Income Sources API](#income-sources-api)
5. [Expenditures API](#expenditures-api)
6. [Error Responses](#error-responses)

---

## Expenses API

### 1. List All Expenses

**Endpoint:** `GET /expenses/api/expenses-api/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 10)
- `category` (optional): Filter by category ID
- `date_after` (optional): Filter by date (YYYY-MM-DD)
- `date_before` (optional): Filter by date (YYYY-MM-DD)

**Example Request:**
```bash
GET /expenses/api/expenses-api/?page=1&page_size=10&category=1
```

**Success Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/expenses/api/expenses-api/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "john_doe"
      },
      "category": {
        "id": 1,
        "name": "Food"
      },
      "member": {
        "id": 2,
        "name": "Jane Doe"
      },
      "amount": "500.00",
      "description": "Groceries shopping",
      "date": "2026-01-15",
      "is_recurring": false,
      "recurring_frequency": null,
      "recurring_end_date": null,
      "created_at": "2026-01-15T10:30:00Z",
      "updated_at": "2026-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "user": {
        "id": 1,
        "username": "john_doe"
      },
      "category": {
        "id": 2,
        "name": "Transport"
      },
      "member": null,
      "amount": "200.00",
      "description": "Taxi fare",
      "date": "2026-01-14",
      "is_recurring": false,
      "recurring_frequency": null,
      "recurring_end_date": null,
      "created_at": "2026-01-14T15:20:00Z",
      "updated_at": "2026-01-14T15:20:00Z"
    }
  ]
}
```

---

### 2. Create Expense

**Endpoint:** `POST /expenses/api/expenses-api/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "amount": "500.00",
  "category": 1,
  "member": 2,
  "date": "2026-01-15",
  "description": "Groceries shopping",
  "is_recurring": false,
  "recurring_frequency": null,
  "recurring_end_date": null
}
```

**Required Fields:**
- `amount` (decimal): Expense amount
- `date` (date): Expense date (YYYY-MM-DD)

**Optional Fields:**
- `category` (integer): Category ID
- `member` (integer): Family member ID
- `description` (string): Expense description
- `is_recurring` (boolean): Is recurring expense
- `recurring_frequency` (string): daily, weekly, monthly, yearly
- `recurring_end_date` (date): End date for recurring

**Success Response (201 Created):**
```json
{
  "id": 3,
  "user": {
    "id": 1,
    "username": "john_doe"
  },
  "category": {
    "id": 1,
    "name": "Food"
  },
  "member": {
    "id": 2,
    "name": "Jane Doe"
  },
  "amount": "500.00",
  "description": "Groceries shopping",
  "date": "2026-01-15",
  "is_recurring": false,
  "recurring_frequency": null,
  "recurring_end_date": null,
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T10:30:00Z"
}
```

---

### 3. Get Expense Details

**Endpoint:** `GET /expenses/api/expenses-api/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Example Request:**
```bash
GET /expenses/api/expenses-api/1/
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "category": {
    "id": 1,
    "name": "Food"
  },
  "member": {
    "id": 2,
    "name": "Jane Doe",
    "role": "Member",
    "phone": "01712345678"
  },
  "amount": "500.00",
  "description": "Groceries shopping",
  "date": "2026-01-15",
  "is_recurring": false,
  "recurring_frequency": null,
  "recurring_end_date": null,
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T10:30:00Z"
}
```

---

### 4. Update Expense (Full Update)

**Endpoint:** `PUT /expenses/api/expenses-api/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "amount": "600.00",
  "category": 1,
  "member": 2,
  "date": "2026-01-15",
  "description": "Groceries shopping - Updated",
  "is_recurring": false
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "john_doe"
  },
  "category": {
    "id": 1,
    "name": "Food"
  },
  "member": {
    "id": 2,
    "name": "Jane Doe"
  },
  "amount": "600.00",
  "description": "Groceries shopping - Updated",
  "date": "2026-01-15",
  "is_recurring": false,
  "recurring_frequency": null,
  "recurring_end_date": null,
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T14:45:00Z"
}
```

---

### 5. Partial Update Expense

**Endpoint:** `PATCH /expenses/api/expenses-api/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body (Only fields to update):**
```json
{
  "amount": "550.00",
  "description": "Groceries - Partial Update"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "john_doe"
  },
  "category": {
    "id": 1,
    "name": "Food"
  },
  "member": {
    "id": 2,
    "name": "Jane Doe"
  },
  "amount": "550.00",
  "description": "Groceries - Partial Update",
  "date": "2026-01-15",
  "is_recurring": false,
  "recurring_frequency": null,
  "recurring_end_date": null,
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T16:20:00Z"
}
```

---

### 6. Delete Expense

**Endpoint:** `DELETE /expenses/api/expenses-api/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Example Request:**
```bash
DELETE /expenses/api/expenses-api/1/
```

**Success Response (204 No Content):**
```
(Empty response body)
```

---

## Family Members API

### 1. List All Members

**Endpoint:** `GET /expenses/api/members/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "john_doe"
    },
    "name": "John Doe",
    "photo": "https://res.cloudinary.com/demo/image/upload/v1234567890/member_photos/john.jpg",
    "role": "Admin",
    "phone": "01712345678",
    "address": "123 Main Street, Dhaka",
    "income_source": {
      "id": 1,
      "name": "Salary"
    },
    "salary": "50000.00",
    "created_at": "2026-01-01T10:00:00Z",
    "updated_at": "2026-01-01T10:00:00Z"
  },
  {
    "id": 2,
    "user": {
      "id": 1,
      "username": "john_doe"
    },
    "name": "Jane Doe",
    "photo": null,
    "role": "Member",
    "phone": "01798765432",
    "address": "123 Main Street, Dhaka",
    "income_source": null,
    "salary": null,
    "created_at": "2026-01-02T11:00:00Z",
    "updated_at": "2026-01-02T11:00:00Z"
  }
]
```

---

### 2. Create Member

**Endpoint:** `POST /expenses/api/members/`

**Request Headers:**
```json
{
  "Content-Type": "multipart/form-data",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body (Form Data):**
```
name: John Doe
role: Member
phone: 01712345678
address: 123 Main Street, Dhaka
income_source: 1
salary: 50000.00
photo: [file upload]
```

**Request Body (JSON - without photo):**
```json
{
  "name": "John Doe",
  "role": "Member",
  "phone": "01712345678",
  "address": "123 Main Street, Dhaka",
  "income_source": 1,
  "salary": "50000.00"
}
```

**Required Fields:**
- `name` (string): Member name

**Optional Fields:**
- `photo` (file): Profile photo
- `role` (string): Admin, Member, Visitor
- `phone` (string): Phone number
- `address` (string): Address
- `income_source` (integer): Income source ID
- `salary` (decimal): Salary amount

**Success Response (201 Created):**
```json
{
  "id": 3,
  "user": {
    "id": 1,
    "username": "john_doe"
  },
  "name": "John Doe",
  "photo": "https://res.cloudinary.com/demo/image/upload/v1234567890/member_photos/john.jpg",
  "role": "Member",
  "phone": "01712345678",
  "address": "123 Main Street, Dhaka",
  "income_source": {
    "id": 1,
    "name": "Salary"
  },
  "salary": "50000.00",
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T10:30:00Z"
}
```

---

### 3. Get Member Details

**Endpoint:** `GET /expenses/api/members/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "name": "John Doe",
  "photo": "https://res.cloudinary.com/demo/image/upload/v1234567890/member_photos/john.jpg",
  "role": "Admin",
  "phone": "01712345678",
  "address": "123 Main Street, Dhaka",
  "income_source": {
    "id": 1,
    "name": "Salary"
  },
  "salary": "50000.00",
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-01T10:00:00Z"
}
```

---

### 4. Update Member

**Endpoint:** `PUT /expenses/api/members/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "name": "John Doe Updated",
  "role": "Admin",
  "phone": "01712345678",
  "address": "456 New Street, Dhaka",
  "income_source": 1,
  "salary": "60000.00"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "john_doe"
  },
  "name": "John Doe Updated",
  "photo": "https://res.cloudinary.com/demo/image/upload/v1234567890/member_photos/john.jpg",
  "role": "Admin",
  "phone": "01712345678",
  "address": "456 New Street, Dhaka",
  "income_source": {
    "id": 1,
    "name": "Salary"
  },
  "salary": "60000.00",
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-15T14:30:00Z"
}
```

---

### 5. Delete Member

**Endpoint:** `DELETE /expenses/api/members/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (204 No Content):**
```
(Empty response body)
```

---

## Categories API

### 1. List All Categories

**Endpoint:** `GET /expenses/api/categories/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Food"
  },
  {
    "id": 2,
    "name": "Transport"
  },
  {
    "id": 3,
    "name": "Entertainment"
  },
  {
    "id": 4,
    "name": "Healthcare"
  },
  {
    "id": 5,
    "name": "Education"
  }
]
```

---

### 2. Create Category

**Endpoint:** `POST /expenses/api/categories/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "name": "Entertainment"
}
```

**Required Fields:**
- `name` (string): Category name (unique)

**Success Response (201 Created):**
```json
{
  "id": 6,
  "name": "Entertainment"
}
```

---

### 3. Get Category Details

**Endpoint:** `GET /expenses/api/categories/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Food"
}
```

---

### 4. Update Category

**Endpoint:** `PUT /expenses/api/categories/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "name": "Food & Beverages"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Food & Beverages"
}
```

---

### 5. Delete Category

**Endpoint:** `DELETE /expenses/api/categories/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (204 No Content):**
```
(Empty response body)
```

**Note:** Cannot delete category if expenses are using it.

---

## Income Sources API

### 1. List All Income Sources

**Endpoint:** `GET /expenses/api/income-sources/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Salary"
  },
  {
    "id": 2,
    "name": "Business"
  },
  {
    "id": 3,
    "name": "Freelancing"
  },
  {
    "id": 4,
    "name": "Investment"
  }
]
```

---

### 2. Create Income Source

**Endpoint:** `POST /expenses/api/income-sources/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "name": "Freelancing"
}
```

**Required Fields:**
- `name` (string): Income source name (unique)

**Success Response (201 Created):**
```json
{
  "id": 5,
  "name": "Freelancing"
}
```

---

### 3. Get Income Source Details

**Endpoint:** `GET /expenses/api/income-sources/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Salary"
}
```

---

### 4. Update Income Source

**Endpoint:** `PUT /expenses/api/income-sources/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "name": "Monthly Salary"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Monthly Salary"
}
```

---

### 5. Delete Income Source

**Endpoint:** `DELETE /expenses/api/income-sources/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (204 No Content):**
```
(Empty response body)
```

---

## Expenditures API

### 1. List All Expenditures

**Endpoint:** `GET /expenses/api/expenditures/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "member": {
      "id": 1,
      "name": "John Doe"
    },
    "category": {
      "id": 1,
      "name": "Food"
    },
    "amount": "300.00",
    "description": "Monthly grocery",
    "date": "2026-01-15"
  },
  {
    "id": 2,
    "member": {
      "id": 2,
      "name": "Jane Doe"
    },
    "category": {
      "id": 2,
      "name": "Transport"
    },
    "amount": "150.00",
    "description": "Bus fare",
    "date": "2026-01-14"
  }
]
```

---

### 2. Create Expenditure

**Endpoint:** `POST /expenses/api/expenditures/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "member": 1,
  "category": 2,
  "amount": "300.00",
  "description": "Monthly subscription",
  "date": "2026-01-15"
}
```

**Required Fields:**
- `member` (integer): Member ID
- `category` (integer): Category ID
- `amount` (decimal): Amount
- `date` (date): Date (YYYY-MM-DD)

**Optional Fields:**
- `description` (string): Description

**Success Response (201 Created):**
```json
{
  "id": 3,
  "member": {
    "id": 1,
    "name": "John Doe"
  },
  "category": {
    "id": 2,
    "name": "Transport"
  },
  "amount": "300.00",
  "description": "Monthly subscription",
  "date": "2026-01-15"
}
```

---

### 3. Get Expenditure Details

**Endpoint:** `GET /expenses/api/expenditures/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "member": {
    "id": 1,
    "name": "John Doe",
    "role": "Admin"
  },
  "category": {
    "id": 1,
    "name": "Food"
  },
  "amount": "300.00",
  "description": "Monthly grocery",
  "date": "2026-01-15"
}
```

---

### 4. Update Expenditure

**Endpoint:** `PUT /expenses/api/expenditures/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Request Body:**
```json
{
  "member": 1,
  "category": 2,
  "amount": "350.00",
  "description": "Monthly subscription - Updated",
  "date": "2026-01-15"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "member": {
    "id": 1,
    "name": "John Doe"
  },
  "category": {
    "id": 2,
    "name": "Transport"
  },
  "amount": "350.00",
  "description": "Monthly subscription - Updated",
  "date": "2026-01-15"
}
```

---

### 5. Delete Expenditure

**Endpoint:** `DELETE /expenses/api/expenditures/{id}/`

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "Cookie": "sessionid=your-session-id"
}
```

**Success Response (204 No Content):**
```
(Empty response body)
```

---

## Error Responses

### 400 Bad Request

**Scenario:** Invalid data or validation error

**Response:**
```json
{
  "amount": [
    "This field is required."
  ],
  "date": [
    "Date has wrong format. Use YYYY-MM-DD."
  ]
}
```

---

### 401 Unauthorized

**Scenario:** Not authenticated

**Response:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 403 Forbidden

**Scenario:** No permission to access resource

**Response:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 404 Not Found

**Scenario:** Resource not found

**Response:**
```json
{
  "detail": "Not found."
}
```

---

### 500 Internal Server Error

**Scenario:** Server error

**Response:**
```json
{
  "detail": "Internal server error. Please try again later."
}
```

---

## Authentication

### Session-Based Authentication

**Login:**
```bash
POST /expenses/login/
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=secret123
```

**Response:**
```
Set-Cookie: sessionid=abc123xyz; Path=/; HttpOnly
```

**Using Session:**
```bash
GET /expenses/api/expenses-api/
Cookie: sessionid=abc123xyz
```

---

## Filtering & Pagination

### Filtering Examples

**Filter by category:**
```bash
GET /expenses/api/expenses-api/?category=1
```

**Filter by date range:**
```bash
GET /expenses/api/expenses-api/?date_after=2026-01-01&date_before=2026-01-31
```

**Filter by member:**
```bash
GET /expenses/api/expenses-api/?member=2
```

**Combined filters:**
```bash
GET /expenses/api/expenses-api/?category=1&date_after=2026-01-01&member=2
```

---

### Pagination Examples

**Default pagination:**
```bash
GET /expenses/api/expenses-api/?page=2
```

**Custom page size:**
```bash
GET /expenses/api/expenses-api/?page=1&page_size=20
```

---

### Ordering Examples

**Order by date (descending):**
```bash
GET /expenses/api/expenses-api/?ordering=-date
```

**Order by amount (ascending):**
```bash
GET /expenses/api/expenses-api/?ordering=amount
```

---

## Testing with cURL

### Create Expense Example

```bash
curl -X POST http://localhost:8000/expenses/api/expenses-api/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your-session-id" \
  -d '{
    "amount": "500.00",
    "category": 1,
    "date": "2026-01-15",
    "description": "Groceries"
  }'
```

### Update Expense Example

```bash
curl -X PUT http://localhost:8000/expenses/api/expenses-api/1/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your-session-id" \
  -d '{
    "amount": "600.00",
    "category": 1,
    "date": "2026-01-15",
    "description": "Groceries - Updated"
  }'
```

### Delete Expense Example

```bash
curl -X DELETE http://localhost:8000/expenses/api/expenses-api/1/ \
  -H "Cookie: sessionid=your-session-id"
```

---

## Testing with Postman

### Setup

1. Import collection
2. Set base URL: `http://localhost:8000/expenses/api/`
3. Configure authentication (Cookie)
4. Test endpoints

### Example Collection Structure

```
Family Expense API
├── Expenses
│   ├── List Expenses
│   ├── Create Expense
│   ├── Get Expense
│   ├── Update Expense
│   └── Delete Expense
├── Members
│   ├── List Members
│   ├── Create Member
│   ├── Get Member
│   ├── Update Member
│   └── Delete Member
├── Categories
│   ├── List Categories
│   ├── Create Category
│   ├── Get Category
│   ├── Update Category
│   └── Delete Category
└── Income Sources
    ├── List Income Sources
    ├── Create Income Source
    ├── Get Income Source
    ├── Update Income Source
    └── Delete Income Source
```

---

**Version:** 2.0.0  
**Last Updated:** April 2026  
**API Base URL:** `http://localhost:8000/expenses/api/`  
**Authentication:** Session-based (Cookie)

---

**For Questions or Support:**  
Contact: Project Maintainer  
GitHub: https://github.com/Raihanroo/Family_expendeture_Truckers-

---

*This documentation provides complete request and response examples for all API endpoints in the Family Expenditure Management System.*
