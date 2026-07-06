from django.urls import path
from .views import department_list, department_detail, department_create

app_name = 'departments'

urlpatterns = [
    path('', department_list, name='department_list'),
    path('create/', department_create, name='department_create'),
    path('<int:pk>/', department_detail, name='department_detail'),
]