from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'department', 'is_staff', 'is_active_agent']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'department', 'phone', 'profile_picture', 'is_active_agent')}),
    )


admin.site.register(User, CustomUserAdmin)