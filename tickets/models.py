from django.conf import settings
from django.db import models


class TicketCategory(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    ticket_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(TicketCategory, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
    'departments.Department',
    null=True, blank=True,
    on_delete=models.SET_NULL,
    related_name='tickets'
)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_tickets',
        on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name='assigned_tickets',
        on_delete=models.SET_NULL
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{Ticket.objects.count() + 1:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_number} - {self.title}"


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.ticket.ticket_number}"


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/%Y/%m/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.ticket.ticket_number}"


class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='history', on_delete=models.CASCADE)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field_changed = models.CharField(max_length=50)
    old_value = models.CharField(max_length=255, blank=True)
    new_value = models.CharField(max_length=255, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.ticket_number}: {self.field_changed} changed"

    class Meta:
        verbose_name_plural = "Ticket histories"

class ReassignmentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    ticket = models.ForeignKey(Ticket, related_name='reassignment_requests', on_delete=models.CASCADE)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reassignment_requests_made', on_delete=models.CASCADE)
    requested_assignee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reassignment_requests_target', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='reassignment_requests_reviewed', on_delete=models.SET_NULL)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Reassignment request for {self.ticket.ticket_number} -> {self.requested_assignee}"