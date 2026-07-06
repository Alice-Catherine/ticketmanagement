from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tickets.models import Ticket
from notifications.models import Notification


class StaffLoginView(LoginView):
    template_name = 'accounts/login.html'


class StaffLogoutView(LogoutView):
    next_page = 'login'


@login_required
def dashboard_view(request):
    user = request.user

    if user.can_view_all_tickets():
        if user.role == 'admin':
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(department=user.department)
    else:
        tickets = Ticket.objects.filter(created_by=user)

    stats = {
        'total': tickets.count(),
        'open': tickets.filter(status='open').count(),
        'in_progress': tickets.filter(status='in_progress').count(),
        'resolved': tickets.filter(status='resolved').count(),
        'closed': tickets.filter(status='closed').count(),
    }

    notifications = user.notifications.filter(is_read=False)[:5]

    return render(request, 'accounts/dashboard.html', {
        'stats': stats,
        'notifications': notifications,
    })