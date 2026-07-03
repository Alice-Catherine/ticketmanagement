from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm
from .models import Ticket, TicketComment


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('tickets:my_tickets')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})


@login_required
def ticket_detail(request, ticket_number):
    ticket = get_object_or_404(Ticket, ticket_number=ticket_number, created_by=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            TicketComment.objects.create(ticket=ticket, author=request.user, message=message)
            return redirect('tickets:ticket_detail', ticket_number=ticket.ticket_number)

    comments = ticket.comments.all().order_by('created_at')
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'comments': comments})