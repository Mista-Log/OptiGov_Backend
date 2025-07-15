
##This is a live server

API Usage Examples:

1. Citizen Signup:
POST /auth/citizen/signup/
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "phone": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "national_id": "1234567890"
}

2. Organization Signup:
POST /auth/organization/signup/
{
    "username": "acme_org",
    "email": "contact@acme.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "phone": "+1234567890",
    "organization_name": "ACME Organization",
    "organization_type": "ngo",
    "registration_number": "REG123456",
    "contact_person": "Jane Smith",
    "address": "123 Main St, City, State",
    "website": "https://acme.org"
}

3. Admin Signup:
POST /auth/admin/signup/
{
    "username": "admin_user",
    "email": "admin@regulator.gov",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "phone": "+1234567890",
    "department": "Regulatory Affairs",
    "position": "Senior Analyst",
    "employee_id": "EMP001",
    "permissions_level": 3
}

4. Login (any user type):
POST /auth/login/
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}

5. Get Profile:
GET /auth/profile/
Headers: Authorization: Token your-token-here

6. Logout:
POST /auth/logout/
Headers: Authorization: Token your-token-here

Security Features:
- Password validation
- Email uniqueness
- Token-based authentication
- Role-based permissions
- User type segregation
- Profile data protection
"""