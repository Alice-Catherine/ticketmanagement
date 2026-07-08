from django.contrib import admin
from accounts.admin import admin_site
from .models import Department, BusinessUnit


@admin.register(Department, site=admin_site)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'created_at']
    search_fields = ['name']


@admin.register(BusinessUnit, site=admin_site)
class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']