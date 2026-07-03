from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Department Manager'),
        ('agent', 'Support Agent'),
        ('employee', 'Employee/User'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    department = models.ForeignKey(
        'departments.Department',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active_agent = models.BooleanField(default=True)

    def can_view_all_tickets(self):
        return self.role in ['admin', 'manager', 'agent']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"