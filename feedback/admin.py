from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'submitted_by', 'rating', 'submitted_at']
    list_filter = ['rating']