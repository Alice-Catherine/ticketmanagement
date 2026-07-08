from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class RoleBasedAdminSite(admin.AdminSite):
    site_header = "Service Desk Administration"
    site_title = "Service Desk Admin"
    index_title = "Site Administration"

    def has_permission(self, request):
        return request.user.is_active and request.user.role == 'admin'


admin_site = RoleBasedAdminSite(name='custom_admin')


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'department', 'is_staff', 'is_active_agent']
    list_filter = ['role', 'department', 'is_staff', 'is_active_agent']
    fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal Info', {'fields': ( 'email', 'phone', 'profile_picture')}),
    ('Service Desk Info', {'fields': ('role', 'department', 'is_active_agent')}),
    ('Status', {'fields': ('is_active', 'is_staff')}),
)
# Registering the model

admin_site.register(User, CustomUserAdmin)