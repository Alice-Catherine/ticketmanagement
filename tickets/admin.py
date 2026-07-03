from django.contrib import admin
from .models import TicketCategory, Ticket, TicketComment, TicketAttachment, TicketHistory


@admin.register(TicketCategory)
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


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'title', 'department', 'status', 'priority', 'assigned_to', 'created_by', 'created_at']
    list_filter = ['status', 'priority', 'department']
    search_fields = ['ticket_number', 'title', 'description']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']
    inlines = [TicketCommentInline, TicketAttachmentInline, TicketHistoryInline]


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at']


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'uploaded_by', 'uploaded_at']