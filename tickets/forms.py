from django import forms
from .models import Ticket, TicketAttachment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'department', 'priority']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ['file']