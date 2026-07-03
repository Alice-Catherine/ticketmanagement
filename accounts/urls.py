from django.urls import path
from .views import StaffLoginView, StaffLogoutView, dashboard_view

app_name = 'accounts'

urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='login'),
    path('logout/', StaffLogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
