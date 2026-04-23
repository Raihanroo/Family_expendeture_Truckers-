# Authentication API Documentation
## Login & Registration Request/Response Examples

---

## Table of Contents

1. [User Login](#user-login)
2. [Admin Login](#admin-login)
3. [User Registration](#user-registration)
4. [Admin Registration](#admin-registration)
5. [Logout](#logout)
6. [CSRF Token Handling](#csrf-token-handling)
7. [Common Errors](#common-errors)

---

## User Login

### Endpoint
```
POST /expenses/login/
```

### Method 1: Form-Based Login (Recommended)

**Request Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: <csrf_token>
Cookie: csrftoken=<csrf_token>
```

**Request Body (Form Data):**
```
username=john_doe
password=secret123
```

**cURL Example:**
```bash
# Step 1: Get CSRF token
curl -c cookies.txt http://localhost:8000/expenses/login/

# Step 2: Extract CSRF token from cookies.txt and login
curl -b cookies.txt -c cookies.txt \
  -X POST http://localhost:8000/expenses/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-CSRFToken: <csrf_token_from_cookies>" \
  -d "username=john_doe&password=secret123"
```

**Success Response (302 Redirect):**
```
HTTP/1.1 302 Found
Location: /expenses/
Set-Cookie: sessionid=abc123xyz456; Path=/; HttpOnly
Set-Cookie: csrftoken=def789ghi012; Path=/
```

**After Redirect (200 OK):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Family Expense</title>
</head>
<body>
    <!-- User Dashboard HTML -->
</body>
</html>
```

---

### Method 2: JSON-Based Login (For API Clients)

**Note:** Django's default login view doesn't support JSON. You need to use session authentication or create a custom API endpoint.

**Alternative: Use Django REST Framework Token Authentication**

First, install and configure DRF token auth, then:

**Request:**
```json
POST /api/auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secret123"
}
```

**Success Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_superuser": false
  }
}
```

---

### Method 3: Postman/Thunder Client

**Step 1: Get CSRF Token**

```
GET http://localhost:8000/expenses/login/
```

**Response Headers:**
```
Set-Cookie: csrftoken=abc123xyz; Path=/
```

**Step 2: Login with CSRF Token**

```
POST http://localhost:8000/expenses/login/
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: abc123xyz
Cookie: csrftoken=abc123xyz

Body (x-www-form-urlencoded):
username: john_doe
password: secret123
```

**Success Response:**
```
HTTP/1.1 302 Found
Location: /expenses/
Set-Cookie: sessionid=def456ghi; Path=/; HttpOnly
```

---

### Login Error Responses

**Invalid Credentials (200 OK with error message):**
```html
<!DOCTYPE html>
<html>
<body>
    <div class="alert alert-danger">
        Invalid username or password
    </div>
    <!-- Login form -->
</body>
</html>
```

**Missing CSRF Token (403 Forbidden):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>Forbidden (403)</h1>
    <p>CSRF verification failed. Request aborted.</p>
</body>
</html>
```

---

## Admin Login

### Endpoint
```
POST /expenses/admin-login/
```

**Request Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: <csrf_token>
Cookie: csrftoken=<csrf_token>
```

**Request Body:**
```
username=raihan12
password=admin123
```

**cURL Example:**
```bash
# Step 1: Get CSRF token
curl -c cookies.txt http://localhost:8000/expenses/admin-login/

# Step 2: Login
curl -b cookies.txt -c cookies.txt \
  -X POST http://localhost:8000/expenses/admin-login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-CSRFToken: <csrf_token>" \
  -d "username=raihan12&password=admin123"
```

**Success Response (302 Redirect):**
```
HTTP/1.1 302 Found
Location: /expenses/admin-dashboard/
Set-Cookie: sessionid=xyz789abc; Path=/; HttpOnly
```

**Error Response (Not Admin):**
```html
<div class="alert alert-danger">
    Access denied. Admin only.
</div>
```

---

## User Registration

### Endpoint
```
POST /expenses/user-register/
```

**Request Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: <csrf_token>
Cookie: csrftoken=<csrf_token>
```

**Request Body:**
```
username=new_user
email=newuser@example.com
password1=strongpassword123
password2=strongpassword123
```

**Required Fields:**
- `username`: Unique username (3-150 characters)
- `email`: Valid email address
- `password1`: Password (min 8 characters)
- `password2`: Password confirmation (must match password1)

**cURL Example:**
```bash
curl -b cookies.txt -c cookies.txt \
  -X POST http://localhost:8000/expenses/user-register/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-CSRFToken: <csrf_token>" \
  -d "username=new_user&email=newuser@example.com&password1=strongpass123&password2=strongpass123"
```

**Success Response (302 Redirect):**
```
HTTP/1.1 302 Found
Location: /expenses/login/
```

**Success Message:**
```html
<div class="alert alert-success">
    Registration successful! Please login.
</div>
```

**Error Response (Username exists):**
```html
<div class="alert alert-danger">
    <ul>
        <li>A user with that username already exists.</li>
    </ul>
</div>
```

**Error Response (Password mismatch):**
```html
<div class="alert alert-danger">
    <ul>
        <li>The two password fields didn't match.</li>
    </ul>
</div>
```

---

## Admin Registration

### Endpoint
```
POST /expenses/register/
```

**Request Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: <csrf_token>
Cookie: csrftoken=<csrf_token>
```

**Request Body:**
```
username=new_admin
email=admin@example.com
password1=adminpass123
password2=adminpass123
admin_secret=change-this-to-a-strong-secret
```

**Required Fields:**
- `username`: Unique username
- `email`: Valid email address
- `password1`: Password
- `password2`: Password confirmation
- `admin_secret`: Admin secret key (from .env file)

**cURL Example:**
```bash
curl -b cookies.txt -c cookies.txt \
  -X POST http://localhost:8000/expenses/register/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-CSRFToken: <csrf_token>" \
  -d "username=new_admin&email=admin@example.com&password1=adminpass123&password2=adminpass123&admin_secret=change-this-to-a-strong-secret"
```

**Success Response (302 Redirect):**
```
HTTP/1.1 302 Found
Location: /expenses/admin-login/
```

**Error Response (Invalid Secret):**
```html
<div class="alert alert-danger">
    Invalid admin secret key
</div>
```

**Error Response (Max Admins Reached):**
```html
<div class="alert alert-danger">
    Maximum number of admins reached
</div>
```

---

## Logout

### Endpoint
```
GET /expenses/logout/
```

**Request Headers:**
```
Cookie: sessionid=<session_id>
```

**cURL Example:**
```bash
curl -b cookies.txt \
  http://localhost:8000/expenses/logout/
```

**Success Response (302 Redirect):**
```
HTTP/1.1 302 Found
Location: /expenses/login/
Set-Cookie: sessionid=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/
```

---

## CSRF Token Handling

### What is CSRF Token?

CSRF (Cross-Site Request Forgery) token is a security measure to prevent unauthorized requests.

### How to Get CSRF Token

**Method 1: From Cookie**

```bash
# Make GET request to any page
curl -c cookies.txt http://localhost:8000/expenses/login/

# Check cookies.txt file
cat cookies.txt
# Output: localhost	FALSE	/	FALSE	0	csrftoken	abc123xyz
```

**Method 2: From HTML Form**

```html
<form method="POST">
    <input type="hidden" name="csrfmiddlewaretoken" value="abc123xyz">
    <!-- Other form fields -->
</form>
```

**Method 3: From Response Header**

```
Set-Cookie: csrftoken=abc123xyz; Path=/
```

### How to Use CSRF Token

**In cURL:**
```bash
curl -X POST http://localhost:8000/expenses/login/ \
  -H "X-CSRFToken: abc123xyz" \
  -H "Cookie: csrftoken=abc123xyz" \
  -d "username=user&password=pass"
```

**In Postman:**
1. Add Header: `X-CSRFToken: abc123xyz`
2. Add Cookie: `csrftoken=abc123xyz`

**In JavaScript (Fetch API):**
```javascript
// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Make POST request
fetch('/expenses/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrftoken
    },
    body: 'username=user&password=pass'
});
```

---

## Common Errors

### 1. 403 Forbidden - CSRF Verification Failed

**Error:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>Forbidden (403)</h1>
    <p>CSRF verification failed. Request aborted.</p>
</body>
</html>
```

**Solution:**
- Include CSRF token in request header: `X-CSRFToken`
- Include CSRF token in cookie: `csrftoken`

---

### 2. 401 Unauthorized - Not Authenticated

**Error:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Solution:**
- Login first to get session cookie
- Include session cookie in subsequent requests

---

### 3. 400 Bad Request - Invalid Data

**Error:**
```html
<div class="alert alert-danger">
    <ul>
        <li>This field is required.</li>
    </ul>
</div>
```

**Solution:**
- Check all required fields are provided
- Verify data format is correct

---

## Complete Login Flow Example

### Step 1: Get CSRF Token

**Request:**
```bash
curl -c cookies.txt -v http://localhost:8000/expenses/login/
```

**Response:**
```
< HTTP/1.1 200 OK
< Set-Cookie: csrftoken=abc123xyz; Path=/
< Content-Type: text/html; charset=utf-8
```

### Step 2: Extract CSRF Token

From `cookies.txt`:
```
localhost	FALSE	/	FALSE	0	csrftoken	abc123xyz
```

### Step 3: Login with CSRF Token

**Request:**
```bash
curl -b cookies.txt -c cookies.txt -v \
  -X POST http://localhost:8000/expenses/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-CSRFToken: abc123xyz" \
  -d "username=john_doe&password=secret123"
```

**Response:**
```
< HTTP/1.1 302 Found
< Location: /expenses/
< Set-Cookie: sessionid=def456ghi; Path=/; HttpOnly
```

### Step 4: Access Protected Resources

**Request:**
```bash
curl -b cookies.txt \
  http://localhost:8000/expenses/api/expenses-api/
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [...]
}
```

---

## Postman Collection Example

### 1. Get CSRF Token

```
GET http://localhost:8000/expenses/login/

Tests:
pm.test("Get CSRF Token", function() {
    var csrftoken = pm.cookies.get("csrftoken");
    pm.environment.set("csrftoken", csrftoken);
});
```

### 2. Login

```
POST http://localhost:8000/expenses/login/

Headers:
X-CSRFToken: {{csrftoken}}

Body (x-www-form-urlencoded):
username: john_doe
password: secret123

Tests:
pm.test("Login Successful", function() {
    pm.response.to.have.status(302);
});
```

### 3. Get Expenses

```
GET http://localhost:8000/expenses/api/expenses-api/

Tests:
pm.test("Get Expenses", function() {
    pm.response.to.have.status(200);
    pm.response.to.be.json;
});
```

---

## Python Requests Example

```python
import requests

# Create session
session = requests.Session()

# Step 1: Get CSRF token
response = session.get('http://localhost:8000/expenses/login/')
csrftoken = session.cookies['csrftoken']

# Step 2: Login
login_data = {
    'username': 'john_doe',
    'password': 'secret123',
    'csrfmiddlewaretoken': csrftoken
}
headers = {
    'X-CSRFToken': csrftoken,
    'Referer': 'http://localhost:8000/expenses/login/'
}
response = session.post(
    'http://localhost:8000/expenses/login/',
    data=login_data,
    headers=headers
)

# Step 3: Access API
response = session.get('http://localhost:8000/expenses/api/expenses-api/')
print(response.json())
```

---

## JavaScript Fetch Example

```javascript
// Step 1: Get CSRF token
async function login(username, password) {
    // Get CSRF token
    const response = await fetch('/expenses/login/');
    const csrftoken = getCookie('csrftoken');
    
    // Step 2: Login
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const loginResponse = await fetch('/expenses/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: formData,
        credentials: 'same-origin'
    });
    
    if (loginResponse.ok) {
        console.log('Login successful');
        // Step 3: Access API
        const apiResponse = await fetch('/expenses/api/expenses-api/', {
            credentials: 'same-origin'
        });
        const data = await apiResponse.json();
        console.log(data);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Usage
login('john_doe', 'secret123');
```

---

**Version:** 2.0.0  
**Last Updated:** April 2026  
**Base URL:** `http://localhost:8000/expenses/`

---

**Important Notes:**
1. Always include CSRF token in POST requests
2. Use session cookies for authentication
3. HTTPS recommended for production
4. Store credentials securely
5. Never expose admin secret key

---

*This documentation provides complete authentication examples with CSRF token handling for the Family Expenditure Management System.*
