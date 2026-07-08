from django.contrib import admin
from accounts.admin import admin_site
from .models import TicketCategory, Ticket, TicketComment, TicketAttachment, TicketHistory, ReassignmentRequest


@admin.register(TicketCategory, site=admin_site)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    readonly_fields = ['author', 'created_at']


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 0
    readonly_fields = ['uploaded_by', 'uploaded_at']


class TicketHistoryInline(admin.TabularInline):
    model = TicketHistory
    extra = 0
    readonly_fields = ['changed_by', 'field_changed', 'old_value', 'new_value', 'changed_at']
    can_delete = False


@admin.register(Ticket, site=admin_site)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'title', 'department', 'status', 'priority', 'assigned_to', 'created_by', 'created_at']
    list_filter = ['status', 'priority', 'department']
    search_fields = ['ticket_number', 'title', 'description']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']
    inlines = [TicketCommentInline, TicketAttachmentInline, TicketHistoryInline]


@admin.register(TicketComment, site=admin_site)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at']


@admin.register(TicketAttachment, site=admin_site)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'uploaded_by', 'uploaded_at']


@admin.register(TicketHistory, site=admin_site)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'field_changed', 'old_value', 'new_value', 'changed_by', 'changed_at']
    list_filter = ['field_changed']


@admin.register(ReassignmentRequest, site=admin_site)
class ReassignmentRequestAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'requested_by', 'requested_assignee', 'status', 'created_at']
    list_filter = ['status']