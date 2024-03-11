from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render, get_list_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from event_ticketing_system.events.models import Event, UserModel
from event_ticketing_system.tickets.forms import TicketPurchaseForm
from event_ticketing_system.tickets.models import Ticket, Purchase


@method_decorator(login_required, name='dispatch')
class TicketPurchaseView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        purchase_form = TicketPurchaseForm(request.POST)

        if purchase_form.is_valid():
            quantity = purchase_form.cleaned_data['quantity']
            ticket_type = purchase_form.cleaned_data['ticket_type']
            ticket = Ticket.objects.get(event=event, ticket_type=ticket_type)

            if ticket.quantity_available > 0:
                price_per_ticket = ticket.price_per_ticket

                if request.user.balance >= quantity * price_per_ticket:
                    success, purchase = TicketPurchaseView.purchase_ticket(request.user, event, quantity, ticket_type)

                    if success:
                        messages.success(request,
                                         f"Successfully purchased {quantity} {ticket.get_ticket_type_display()} ticket(s) for {event.title}.")
                        return redirect(reverse('ticket_purchase_success', kwargs={'pk': event.pk}))
                    else:
                        messages.error(request, "Failed to complete the purchase.")
                        return redirect('ticket_purchase_failure')
                else:
                    messages.error(request, "Insufficient balance to purchase tickets.")
                    return redirect('ticket_purchase_failure')
            else:
                messages.error(request, "No tickets available for the selected type.")
                return redirect('ticket_purchase_failure')
        else:
            messages.error(request, "Invalid purchase form submission.")
            return redirect('ticket_purchase_failure')

    @staticmethod
    def purchase_ticket(user, event, quantity, ticket_type):
        ticket = Ticket.objects.get(event=event, ticket_type=ticket_type)

        if ticket.quantity_available >= quantity:
            with transaction.atomic():
                purchase = Purchase.objects.create(
                    user=user,
                    ticket=ticket,
                    quantity=quantity
                )

                ticket.quantity_available -= quantity
                ticket.save()

                user.balance -= quantity * ticket.price_per_ticket
                user.save()

                return True, purchase

        return False, None


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
        # Get all error messages
        error_messages = [message.message for message in messages.get_messages(request) if
                          message.level == messages.ERROR]

        # Get the last error message
        last_error_message = error_messages[-1] if error_messages else None

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

            refundable_purchases = ticket.purchase_set.filter(
                user=user,
                refund_deadline__gte=timezone.now()
            )

            refundable_quantity = sum([purchase.quantity for purchase in refundable_purchases])

            user_tickets_quantity_dict[key] = {
                'event_id': ticket.event.id,
                'event__title': ticket.event.title,
                'ticket_type': ticket.get_ticket_type_display(),
                'total_quantity': total_quantity,
                'refundable_quantity': refundable_quantity,
                'price_per_ticket': ticket.price_per_ticket,
                'refundable': refundable_quantity > 0,
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

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        event_id = kwargs['event_id']
        tickets = get_list_or_404(Ticket, event_id=event_id)

        refunded_tickets = []

        for ticket in tickets:
            refundable_purchase = Purchase.objects.filter(
                user=request.user,
                ticket=ticket,
                refund_deadline__gte=timezone.now()
            ).first()

            if refundable_purchase:
                ticket_price_refund = refundable_purchase.quantity * ticket.price_per_ticket

                with transaction.atomic():
                    refundable_purchase.delete()

                    ticket.quantity_available += refundable_purchase.quantity
                    ticket.save()

                    request.user.balance += ticket_price_refund
                    request.user.save()

                    refunded_tickets.append(ticket)

        if refunded_tickets:
            messages.success(request, f"Refund request successful for tickets.")
        else:
            messages.error(request, f"No refundable purchases found for tickets.")

        context = {
            'refunded_tickets': refunded_tickets,
        }

        return render(request, self.template_name, context)
