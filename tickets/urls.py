from django.urls import path
from .views import create_ticket, my_tickets, ticket_detail

app_name = 'tickets'

urlpatterns = [
    path('create/', create_ticket, name='create_ticket'),
    path('my-tickets/', my_tickets, name='my_tickets'),
    path('<str:ticket_number>/', ticket_detail, name='ticket_detail'),
]
