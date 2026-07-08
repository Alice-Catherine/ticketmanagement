from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from tickets.models import Ticket
from notifications.models import Notification
from .forms import EmployeeRegistrationForm


class StaffLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = EmployeeRegistrationForm()
        context['active_tab'] = 'login'
        return context


class StaffLogoutView(LogoutView):
    next_page = 'accounts:login'


def register_view(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = EmployeeRegistrationForm()

    login_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'form': login_form,
        'register_form': form,
        'active_tab': 'register',
    })


@login_required
def dashboard_view(request):
    user = request.user
    can_view_stats = user.role in ['admin', 'manager','agent']

    stats = None
    if can_view_stats:
        if user.role == 'admin':
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(department=user.department)

        stats = {
            'total': tickets.count(),
            'open': tickets.filter(status='open').count(),
            'assigned': tickets.filter(status='assigned').count(),
            'in_progress': tickets.filter(status='in_progress').count(),
            'resolved': tickets.filter(status='resolved').count(),
            'closed': tickets.filter(status='closed').count(),
        }

    notifications = user.notifications.filter(is_read=False)[:5]

    return render(request, 'accounts/dashboard.html', {
        'stats': stats,
        'can_view_stats': can_view_stats,
        'notifications': notifications,
    })