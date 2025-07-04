


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPES = (
        ('citizen', 'Citizen'),
        ('organization', 'Organization'),
        ('admin', 'Admin/Regulator'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class CitizenProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=20, unique=True, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class OrganizationProfile(models.Model):
    ORGANIZATION_TYPES = (
        ('ngo', 'NGO'),
        ('company', 'Company'),
        ('government', 'Government Agency'),
        ('educational', 'Educational Institution'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization_profile')
    organization_name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=20, choices=ORGANIZATION_TYPES)
    registration_number = models.CharField(max_length=50, unique=True)
    contact_person = models.CharField(max_length=100)
    address = models.TextField()
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.organization_name

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    permissions_level = models.IntegerField(default=1)  # 1-5 scale
    
    def __str__(self):
        return f"{self.user.username} - {self.department}"
# # Create your models here.
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.core.validators import RegexValidator

# class User(AbstractUser):
#     USER_ROLES = (
#         ('citizen', 'Citizen'),
#         ('organization', 'Organization'),
#         ('admin', 'Admin'),
#     )
    
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(
#         max_length=15,
#         validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
#         null=True,
#         blank=True
#     )
#     role = models.CharField(max_length=20, choices=USER_ROLES, default='citizen')
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
    
#     def __str__(self):
#         return f"{self.email} ({self.role})"


# class CitizenProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen_profile')
#     date_of_birth = models.DateField()
#     address = models.TextField()
#     gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
#     national_id_number = models.CharField(max_length=20)
#     id_document = models.FileField(upload_to='citizen_ids/')

#     def __str__(self):
#         return f"Citizen Profile: {self.user.email}"

# class OrganizationProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization_profile')
#     company_name = models.CharField(max_length=255)
#     cac_number = models.CharField(max_length=50)
#     tax_id_number = models.CharField(max_length=50)
#     company_address = models.TextField()
#     industry_type = models.CharField(max_length=100)
#     cac_certificate = models.FileField(upload_to='org_docs/')
#     tax_clearance_certificate = models.FileField(upload_to='org_docs/')

#     def __str__(self):
#         return f"Organization: {self.company_name}"



# class AdminProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
#     government_agency = models.CharField(max_length=255)
#     designation = models.CharField(max_length=100)
#     staff_id = models.CharField(max_length=50)
#     official_id = models.FileField(upload_to='admin_ids/')

#     def __str__(self):
#         return f"Admin: {self.user.email}"



# class OTPVerification(models.Model):
#     VERIFICATION_TYPES = (
#         ('email', 'Email'),
#         ('phone', 'Phone'),
#     )
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     verification_type = models.CharField(max_length=10, choices=VERIFICATION_TYPES)
#     code = models.CharField(max_length=6)
#     is_used = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField()
    
#     class Meta:
#         ordering = ['-created_at']




