from django.urls import path
from .views import create_ticket, my_tickets, ticket_detail, approve_reassignment, reject_reassignment

app_name = 'tickets'

urlpatterns = [
    path('create/', create_ticket, name='create_ticket'),
    path('my-tickets/', my_tickets, name='my_tickets'),
    path('reassignment/<int:request_id>/approve/', approve_reassignment, name='approve_reassignment'),
    path('reassignment/<int:request_id>/reject/', reject_reassignment, name='reject_reassignment'),
    path('<str:ticket_number>/', ticket_detail, name='ticket_detail'),
]