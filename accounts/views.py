from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class StaffLoginView(LoginView):
    template_name = 'accounts/login.html'


class StaffLogoutView(LogoutView):
    next_page = 'login'


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')