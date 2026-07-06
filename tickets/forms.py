from django import forms
from django.contrib.auth import get_user_model
from .models import Ticket, TicketAttachment

User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'department', 'priority']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ['file']


class TicketManageForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'priority', 'assigned_to']

    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if department:
            self.fields['assigned_to'].queryset = User.objects.filter(department=department)