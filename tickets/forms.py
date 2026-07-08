from django import forms
from django.contrib.auth import get_user_model
from .models import Ticket, TicketAttachment, ReassignmentRequest

User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'priority']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ['file']


class TicketManageForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['department', 'status', 'priority', 'assigned_to']

    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if department:
            self.fields['assigned_to'].queryset = User.objects.filter(department=department)
        else:
            self.fields['assigned_to'].queryset = User.objects.filter(role__in=['agent', 'manager'])


class ReassignmentRequestForm(forms.ModelForm):
    class Meta:
        model = ReassignmentRequest
        fields = ['requested_assignee', 'reason']

    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        current_assignee = kwargs.pop('current_assignee', None)
        super().__init__(*args, **kwargs)

        if department:
            queryset = User.objects.filter(department=department)
        else:
            queryset = User.objects.filter(role__in=['agent', 'manager'])

        if current_assignee:
            queryset = queryset.exclude(id=current_assignee.id)

        self.fields['requested_assignee'].queryset = queryset
        self.fields['reason'].widget = forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why should this ticket be reassigned?'})