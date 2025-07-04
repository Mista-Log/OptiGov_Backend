from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CitizenProfile, OrganizationProfile, AdminProfile

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_verified', 'created_at']
    list_filter = ['user_type', 'is_verified', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'email', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(CitizenProfile)
admin.site.register(OrganizationProfile)
admin.site.register(AdminProfile)


# Register your models here.
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import User, OTPVerification, CitizenProfile, OrganizationProfile, AdminProfile

# admin.site.register(CitizenProfile)
# admin.site.register(OrganizationProfile)
# admin.site.register(AdminProfile)


# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('email', 'username', 'phone_number', 'role')

# class CustomUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = User
#         fields = ('email', 'username', 'phone_number', 'role', 'is_verified', 'is_active', 'is_staff')

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     form = CustomUserChangeForm
#     add_form = CustomUserCreationForm
    
#     list_display = ('email', 'username', 'role', 'is_verified', 'is_active', 'is_staff', 'created_at')
#     list_filter = ('role', 'is_verified', 'is_active', 'is_staff', 'created_at')
#     search_fields = ('email', 'username', 'phone_number')
#     ordering = ('-created_at',)
    
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('username', 'phone_number', 'role')}),
#         ('Permissions', {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
#         }),
#         ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
#     )
    
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'phone_number', 'role', 'password1', 'password2'),
#         }),
#     )
    
#     readonly_fields = ('created_at', 'updated_at', 'date_joined', 'last_login')

# @admin.register(OTPVerification)
# class OTPVerificationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'verification_type', 'code', 'is_used', 'created_at', 'expires_at')
#     list_filter = ('verification_type', 'is_used', 'created_at')
#     search_fields = ('user__email', 'user__username', 'code')
#     readonly_fields = ('created_at',)
#     ordering = ('-created_at',)
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('user')