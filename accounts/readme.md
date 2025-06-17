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
