
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_ROLES = (
        ('citizen', 'Citizen'),
        ('organization', 'Organization'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='citizen')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.email} ({self.role})"

class OTPVerification(models.Model):
    VERIFICATION_TYPES = (
        ('email', 'Email'),
        ('phone', 'Phone'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_type = models.CharField(max_length=10, choices=VERIFICATION_TYPES)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']