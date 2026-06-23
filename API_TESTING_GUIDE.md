# API Testing Guide - Basic Authentication

## ✅ Server is Ready!

Your Django server now supports easy API access using Basic Authentication - no CSRF tokens needed!

---

## 🚀 How to Test in Postman

### Step 1: Start the Server
```bash
python manage.py runserver
```

### Step 2: Test Any API Endpoint

**Example: Get Family Members**

1. Create a new request in Postman
2. Set method to `GET`
3. Enter URL: `http://127.0.0.1:8000/expenses/api/members/`
4. Go to "Authorization" tab
5. Select "Basic Auth" from Type dropdown
6. Enter:
   - Username: `raihan`
   - Password: `123456`
7. Click "Send"

**Expected Response:**
```json
[
    {
        "id": 1,
        "name": "John Doe",
        "relationship": "Father",
        "photo": "/media/member_photos/photo.jpg",
        "user": 2
    }
]
```

---

## 📝 Available Test Users

| Username | Password | Type |
|----------|----------|------|
| raihan12 | admin123 | Admin |
| raihan | 123456 | User |
| sagor | test123 | User |

---

## 🔗 All API Endpoints

### Family Members
- `GET /expenses/api/members/` - List all members
- `POST /expenses/api/members/` - Create member
- `GET /expenses/api/members/{id}/` - Get member details
- `PUT /expenses/api/members/{id}/` - Update member
- `DELETE /expenses/api/members/{id}/` - Delete member

### Expenses
- `GET /expenses/api/expenses-api/` - List all expenses
- `POST /expenses/api/expenses-api/` - Create expense
- `GET /expenses/api/expenses-api/{id}/` - Get expense details
- `PUT /expenses/api/expenses-api/{id}/` - Update expense
- `DELETE /expenses/api/expenses-api/{id}/` - Delete expense

### Categories
- `GET /expenses/api/categories/` - List all categories
- `POST /expenses/api/categories/` - Create category
- `GET /expenses/api/categories/{id}/` - Get category details
- `PUT /expenses/api/categories/{id}/` - Update category
- `DELETE /expenses/api/categories/{id}/` - Delete category

### Income Sources
- `GET /expenses/api/income-sources/` - List all income sources
- `POST /expenses/api/income-sources/` - Create income source
- `GET /expenses/api/income-sources/{id}/` - Get income source details
- `PUT /expenses/api/income-sources/{id}/` - Update income source
- `DELETE /expenses/api/income-sources/{id}/` - Delete income source

### Expenditures
- `GET /expenses/api/expenditures/` - List all expenditures
- `POST /expenses/api/expenditures/` - Create expenditure
- `GET /expenses/api/expenditures/{id}/` - Get expenditure details
- `PUT /expenses/api/expenditures/{id}/` - Update expenditure
- `DELETE /expenses/api/expenditures/{id}/` - Delete expenditure

---

## 🧪 Testing POST Request

**Example: Create a New Family Member**

1. Method: `POST`
2. URL: `http://127.0.0.1:8000/expenses/api/members/`
3. Authorization: Basic Auth (raihan / 123456)
4. Headers:
   - `Content-Type: application/json`
5. Body (raw JSON):
```json
{
    "name": "Jane Doe",
    "relationship": "Mother"
}
```

---

## 🐍 Testing with Python

```python
import requests
from requests.auth import HTTPBasicAuth

# Base configuration
BASE_URL = 'http://127.0.0.1:8000/expenses/api'
auth = HTTPBasicAuth('raihan', '123456')

# GET request
response = requests.get(f'{BASE_URL}/members/', auth=auth)
print(response.json())

# POST request
new_member = {
    'name': 'Jane Doe',
    'relationship': 'Mother'
}
response = requests.post(
    f'{BASE_URL}/members/',
    json=new_member,
    auth=auth
)
print(response.json())
```

---

## 🔧 Testing with cURL

```bash
# GET request
curl -X GET http://127.0.0.1:8000/expenses/api/members/ \
  -u raihan:123456

# POST request
curl -X POST http://127.0.0.1:8000/expenses/api/members/ \
  -u raihan:123456 \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","relationship":"Mother"}'
```

---

## ❌ Common Issues

### Issue: 401 Unauthorized
**Solution:** Check username and password are correct

### Issue: 403 Forbidden
**Solution:** Make sure you're using Basic Auth, not trying to send credentials in body

### Issue: Connection refused
**Solution:** Make sure Django server is running on port 8000

---

## ✨ What Changed?

- ✅ BasicAuthentication enabled in settings.py
- ✅ No CSRF token required for API endpoints
- ✅ Simple username:password authentication
- ✅ Works with Postman, cURL, Python requests, etc.
- ✅ All ViewSets properly configured

---

## 📚 More Information

- Full API documentation: `API_REQUEST_RESPONSE_DOCUMENTATION.md`
- Authentication details: `AUTHENTICATION_API_DOCUMENTATION.md`
- Complete project docs: `COMPLETE_PROJECT_DOCUMENTATION.md`
