from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render, get_list_or_404
from django.urls import reverse
from django.utils import timezone
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
                return redirect(
                    reverse('event_details', kwargs={'pk': event.pk}))
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
        # Get the last error message
        error_messages = [m for m in messages.get_messages(request) if m.level == messages.ERROR]
        last_error_message = error_messages[-1].message if error_messages else None

        return render(request, self.template_name, {'error_message': last_error_message})


class UserTicketsView(View):
    template_name = 'accounts/user_tickets.html'

    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])

        user_tickets = Ticket.objects.filter(purchase__user=user)

        user_tickets_quantity_dict = {}

        processed_tickets = set()

        for ticket in user_tickets:
            key = (ticket.event.id, ticket.get_ticket_type_display())

            if key in processed_tickets:
                continue

            total_quantity = sum([purchase.quantity for purchase in ticket.purchase_set.filter(user=user)])

            user_tickets_quantity_dict[key] = {
                'event_id': ticket.event.id,
                'event__title': ticket.event.title,
                'ticket_type': ticket.get_ticket_type_display(),
                'total_quantity': total_quantity,
                'price_per_ticket': ticket.price_per_ticket,
                'refundable': any(
                    purchase.refund_deadline >= timezone.now() for purchase in ticket.purchase_set.filter(user=user)),
            }

            # Mark the ticket type as processed
            processed_tickets.add(key)

        user_tickets_quantity = list(user_tickets_quantity_dict.values())

        context = {
            'user_tickets_quantity': user_tickets_quantity,
        }

        return render(request, self.template_name, context)


class RefundTicketView(View):
    template_name = 'tickets/refund_ticket.html'

    def get(self, request, *args, **kwargs):
        event_id = kwargs['event_id']
        tickets = get_list_or_404(Ticket, event_id=event_id)

        context = {
            'tickets': tickets,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        event_id = kwargs['event_id']
        tickets = get_list_or_404(Ticket, event_id=event_id)

        refundable_purchases = []

        for ticket in tickets:
            refundable_purchase = Purchase.objects.filter(
                user=request.user,
                ticket=ticket,
                refund_deadline__gte=timezone.now()
            ).first()

            if refundable_purchase:
                refundable_purchases.append(refundable_purchase)

        refunded_tickets = []

        if refundable_purchases:
            for refundable_purchase in refundable_purchases:
                refundable_purchase.delete()
                ticket = refundable_purchase.ticket
                ticket.quantity_available += refundable_purchase.quantity
                ticket.save()
                refunded_tickets.append(ticket)

            messages.success(request, f"Refund request successful for tickets.")
        else:
            messages.error(request, f"No refundable purchases found for tickets.")

        # Render the same template with updated context
        context = {
            'refunded_tickets': refunded_tickets,
        }

        return render(request, self.template_name, context)
