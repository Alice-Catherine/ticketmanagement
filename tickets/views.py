from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import TicketForm, AttachmentForm, TicketManageForm
from .models import Ticket, TicketComment
from notifications.models import Notification


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
    if request.user.can_view_all_tickets():
        if request.user.role == 'admin':
            tickets = Ticket.objects.all().order_by('-created_at')
        else:
            tickets = Ticket.objects.filter(department=request.user.department).order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})


@login_required
def ticket_detail(request, ticket_number):
    ticket = get_object_or_404(Ticket, ticket_number=ticket_number)

    if not (ticket.created_by == request.user or request.user.can_view_all_tickets()):
        return HttpResponseForbidden("You don't have permission to view this ticket.")

    can_manage = request.user.can_view_all_tickets()
    manage_form = None

    if request.method == 'POST':
        if 'message' in request.POST:
            message = request.POST.get('message')
            if message:
                TicketComment.objects.create(ticket=ticket, author=request.user, message=message)
                return redirect('tickets:ticket_detail', ticket_number=ticket.ticket_number)

        elif 'file' in request.FILES:
            attachment_form = AttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.ticket = ticket
                attachment.uploaded_by = request.user
                attachment.save()
                return redirect('tickets:ticket_detail', ticket_number=ticket.ticket_number)

        elif 'status' in request.POST and can_manage:
            previous_assignee = ticket.assigned_to
            manage_form = TicketManageForm(request.POST, instance=ticket, department=ticket.department)
            if manage_form.is_valid():
                updated_ticket = manage_form.save()

                if updated_ticket.assigned_to and updated_ticket.assigned_to != previous_assignee:
                    Notification.objects.create(
                        user=updated_ticket.assigned_to,
                        ticket=updated_ticket,
                        message=f"You've been assigned ticket {updated_ticket.ticket_number}: {updated_ticket.title}"
                    )

                messages.success(request, "Ticket updated successfully.")
                return redirect('tickets:ticket_detail', ticket_number=ticket.ticket_number)

    if manage_form is None and can_manage:
        manage_form = TicketManageForm(instance=ticket, department=ticket.department)

    comments = ticket.comments.all().order_by('created_at')
    attachments = ticket.attachments.all().order_by('-uploaded_at')
    attachment_form = AttachmentForm()

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'attachments': attachments,
        'attachment_form': attachment_form,
        'manage_form': manage_form,
        'can_manage': can_manage,
    })