# OptiGov API Postman Collection Setup

## 1. Create Collection & Environment

- **Collection Name:** `OptiGov API`
- **Environment Variables:**
    - `base_url`: `http://127.0.0.1:8000`
    - `access_token`: *(set automatically)*
    - `refresh_token`: *(set automatically)*

---

## 2. Postman Requests

### 1. Register User

- **Method:** `POST`
- **URL:** `{{base_url}}/api/auth/register/`
- **Headers:**
    - `Content-Type: application/json`
- **Body (raw JSON):**
    ```json
    {
        "email": "test@example.com",
        "username": "testuser",
        "phone_number": "+2348012345678",
        "role": "citizen",
        "password": "SecurePassword123!",
        "password_confirm": "SecurePassword123!"
    }
    ```

---

### 2. Request OTP

- **Method:** `POST`
- **URL:** `{{base_url}}/api/auth/otp/request/`
- **Headers:**
    - `Content-Type: application/json`
- **Body (raw JSON):**
    ```json
    {
        "email": "test@example.com",
        "verification_type": "email"
    }
    ```

---

### 3. Verify OTP

- **Method:** `POST`
- **URL:** `{{base_url}}/api/auth/otp/verify/`
- **Headers:**
    - `Content-Type: application/json`
- **Body (raw JSON):**
    ```json
    {
        "email": "test@example.com",
        "code": "123456",
        "verification_type": "email"
    }
    ```
- **Tests (auto-save tokens):**
    ```javascript
    if (pm.response.code === 200) {
            const responseJson = pm.response.json();
            pm.environment.set("access_token", responseJson.access);
            pm.environment.set("refresh_token", responseJson.refresh);
    }
    ```

---

### 4. Login

- **Method:** `POST`
- **URL:** `{{base_url}}/api/auth/login/`
- **Headers:**
    - `Content-Type: application/json`
- **Body (raw JSON):**
    ```json
    {
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }
    ```
- **Tests (auto-save tokens):**
    ```javascript
    if (pm.response.code === 200) {
            const responseJson = pm.response.json();
            pm.environment.set("access_token", responseJson.access);
            pm.environment.set("refresh_token", responseJson.refresh);
    }
    ```

---

### 5. Get Profile (Protected Route)

- **Method:** `GET`
- **URL:** `{{base_url}}/api/auth/profile/`
- **Headers:**
    - `Authorization: Bearer {{access_token}}`

---

**Tip:** Use the "Tests" tab in Postman to add the JavaScript code for auto-saving tokens after login or OTP verification.


# 🇳🇬 Government Services API

This is a role-based Django REST Framework API that supports **Citizens**, **Organizations**, and **Admins** with custom registration, login, and logout functionality.

---

## 🔧 Tech Stack

- Django
- Django REST Framework
- Simple JWT (JSON Web Tokens)
- PostgreSQL (or SQLite for testing)

---

## 📌 Available Roles

- `citizen`
- `organization`
- `admin`

Each role has a different registration and login process, enforced via custom serializers and views.

---

## 📁 API Endpoints

> Base URL: `http://localhost:8000/`

---

## 👤 User Registration

### ➤ 1. Register Citizen

**POST** `/register/citizen/`

#### Payload:
    ```json
    {
    "user": {
        "email": "john@example.com",
        "username": "john_doe",
        "phone_number": "+2347012345678",
        "password": "strong_password"
    },
    "date_of_birth": "1990-01-01",
    "address": "1234 Federal Street, Abuja",
    "gender": "male",
    "national_id_number": "12345678901"
    }
    ```

---


### ➤ 2. Register Organization

**POST** `/register/organization/`

#### Payload:
    ```json
    {
    "user": {
        "email": "org@example.com",
        "username": "org123",
        "phone_number": "+2347012345678",
        "password": "strong_password"
    },
    "company_name": "TechGov Ltd.",
    "cac_number": "CAC1234567",
    "tax_id_number": "TIN123456",
    "company_address": "10 Broad Street, Lagos",
    "industry_type": "Software Development"
    }
    ```

---

### ➤ 3. Register Admin (Restricted)

**POST** `/register/admin/`

#### Payload:
    ```json
    {
    "user": {
        "email": "admin@gov.ng",
        "username": "admin1",
        "phone_number": "+2347012345678",
        "password": "admin_password"
    },
    "government_agency": "NITDA",
    "designation": "Data Officer",
    "staff_id": "GOV12345"
    }

    ```

---

##🔐 Login (JWT Authentication)

### ➤ 4. Login as Citizen

**POST** `/login/citizen/`

#### Payload:
    ```json
    {
    "email": "john@example.com",
    "password": "strong_password"
    }


    ```

---

### ➤ 5. Login as Organization

**POST** `/login/organization/`

#### Payload:
    ```json
    {
    "email": "org@example.com",
    "password": "strong_password"
    }
    ```

---

### ➤ 6. Login as Admin

**POST** `/login/admin/`

#### Payload:
    ```json
    {
    "email": "admin@gov.ng",
    "password": "admin_password"
    }

    ```

---


###🚪 Logout (All Roles)

**POST** `/logout/`

#### Payload:
    ```json
    {
    "refresh_token": "your-refresh-token"
    }
    ```

---

