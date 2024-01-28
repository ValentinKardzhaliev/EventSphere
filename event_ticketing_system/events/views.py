from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventAddForm, TicketPurchaseForm
from ..tickets.models import Purchase, Ticket


@method_decorator(login_required, name='dispatch')
class EventAddView(CreateView):
    model = Event
    form_class = EventAddForm
    template_name = 'events/event_add.html'
    success_url = reverse_lazy('index')  # Adjust 'event_list' to the actual URL name for your events list

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventDetailsView(DetailView):
    model = Event
    template_name = 'events/event_details.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase_form'] = TicketPurchaseForm()
        return context

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        purchase_form = TicketPurchaseForm(request.POST)

        if purchase_form.is_valid():
            quantity = purchase_form.cleaned_data['quantity']

            # Get the specific ticket associated with the event (VIP or Regular)
            ticket_type = purchase_form.cleaned_data['ticket_type']
            ticket = Ticket.objects.get(event=event, ticket_type=ticket_type)

            # Check if there are enough available tickets
            if ticket.quantity_available >= quantity:
                # Create a purchase record
                purchase = Purchase.objects.create(
                    user=request.user,
                    ticket=ticket,
                    quantity=quantity
                )

                # Update the quantity of available tickets
                ticket.quantity_available -= quantity
                ticket.save()

                messages.success(request,
                                 f"Successfully purchased {quantity} {ticket.get_ticket_type_display()} ticket(s) for {event.title}.")
                return redirect('event_details', pk=event.pk)
            else:
                messages.error(request,
                               f"Insufficient available {ticket.get_ticket_type_display()} tickets for {event.title}.")
        else:
            messages.error(request, "Invalid purchase form submission.")

        return self.render_to_response(self.get_context_data())


class PurchaseSuccessView(View):
    template_name = 'events/ticket_purchase_success.html'

    def get(self, request, *args, **kwargs):
        success_message = messages.get_messages(request).first()
        return render(request, self.template_name, {'success_message': success_message})


class PurchaseFailureView(View):
    template_name = 'events/purchase_failure'

    def get(self, request, *args, **kwargs):
        error_message = messages.get_messages(request).first()
        return render(request, self.template_name, {'error_message': error_message})


@login_required
def user_created_events(request):
    events_created_by_user = Event.objects.filter(creator=request.user)
    context = {'user_created_events': events_created_by_user}
    return render(request, 'events/user_created_events.html', context)
