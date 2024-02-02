from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View

from event_ticketing_system.events.forms import TicketPurchaseForm
from event_ticketing_system.events.models import Event, UserModel
from event_ticketing_system.tickets.models import Ticket, Purchase


@method_decorator(login_required, name='dispatch')
class TicketPurchaseView(View):
    template_name = 'tickets/purchase_ticket.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        purchase_form = TicketPurchaseForm(request.POST)

        if purchase_form.is_valid():
            quantity = purchase_form.cleaned_data['quantity']
            ticket_type = purchase_form.cleaned_data['ticket_type']
            ticket = Ticket.objects.get(event=event, ticket_type=ticket_type)

            if ticket.quantity_available >= quantity:
                purchase = Purchase.objects.create(
                    user=request.user,
                    ticket=ticket,
                    quantity=quantity
                )

                ticket.quantity_available -= quantity
                ticket.save()

                messages.success(request,
                                 f"Successfully purchased {quantity} {ticket.get_ticket_type_display()} ticket(s) for {event.title}.")
                return redirect('ticket_purchase_success', pk=event.pk)
            else:
                if ticket.quantity_available == 0:
                    messages.error(request,
                                   f"There are no more {ticket.get_ticket_type_display()} tickets available for {event.title}.")
                else:
                    messages.error(request,
                                   f"Insufficient available {ticket.get_ticket_type_display()} tickets for {event.title}.")
                return redirect('ticket_purchase_failure')
        else:
            messages.error(request, "Invalid purchase form submission.")
            return render(request, self.template_name, {'purchase_form': purchase_form, 'event': event})


class TicketPurchaseSuccessView(View):
    template_name = 'tickets/ticket_purchase_success.html'

    def get(self, request, *args, **kwargs):
        # Get the last success message
        success_messages = [m for m in messages.get_messages(request) if m.level == messages.SUCCESS]
        last_success_message = success_messages[-1].message if success_messages else None

        return render(request, self.template_name, {'success_message': last_success_message})


class TicketPurchaseFailureView(View):
    template_name = 'tickets/ticket_purchase_failure.html'

    def get(self, request, *args, **kwargs):
        error_message = messages.get_messages(request)
        return render(request, self.template_name, {'error_message': error_message})


class UserTicketsView(View):
    template_name = 'tickets/user_tickets.html'

    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])

        user_tickets = Ticket.objects.filter(purchase__user=user)

        user_tickets_quantity_dict = {}

        processed_tickets = set()

        for ticket in user_tickets:
            key = (ticket.event.title, ticket.get_ticket_type_display())

            if key in processed_tickets:
                continue

            total_quantity = sum([purchase.quantity for purchase in ticket.purchase_set.filter(user=user)])

            user_tickets_quantity_dict[key] = {
                'event__title': ticket.event.title,
                'ticket_type': ticket.get_ticket_type_display(),
                'total_quantity': total_quantity,
                'price_per_ticket': ticket.price_per_ticket,
            }

            # Mark the ticket type as processed
            processed_tickets.add(key)

        user_tickets_quantity = list(user_tickets_quantity_dict.values())

        context = {
            'user_tickets_quantity': user_tickets_quantity,
        }

        return render(request, self.template_name, context)
