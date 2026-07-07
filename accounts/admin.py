from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .models import User


class RoleBasedAdminSite(admin.AdminSite):
    site_header = "Service Desk Administration"
    site_title = "Service Desk Admin"
    index_title = "Site Administration"

    def has_permission(self, request):
        return request.user.is_active and request.user.role == 'admin'

    def logout(self, request, extra_context=None):
        return LogoutView.as_view(next_page=reverse_lazy('custom_admin:login'))(request)


admin_site = RoleBasedAdminSite(name='custom_admin')

admin_site.register(User, UserAdmin)