from dal import autocomplete
from cities_light.models import City
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventAddForm, TicketPurchaseForm
from ..common.models import Like
from ..tickets.forms import TicketForm, VipTicketForm
from ..tickets.models import Ticket


@method_decorator(login_required, name='dispatch')
class EventAddView(CreateView):
    model = Event
    form_class = EventAddForm
    template_name = 'events/event_add.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize forms with the current request POST data
        context['ticket_form'] = TicketForm(self.request.POST)
        context['vip_ticket_form'] = VipTicketForm(self.request.POST, show_vip_fields=False)
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user

        # Create instances of the ticket forms
        ticket_form = TicketForm(self.request.POST)
        vip_ticket_form = VipTicketForm(self.request.POST,
                                        show_vip_fields=self.request.POST.get('toggleVipTickets') == 'Add VIP Tickets')

        # Validate all forms
        if form.is_valid() and ticket_form.is_valid() and vip_ticket_form.is_valid():
            event = form.save()

            ticket = ticket_form.save(commit=False)
            ticket.event = event
            ticket.save()

            vip_ticket = vip_ticket_form.save(commit=False)
            vip_ticket.event = event
            vip_ticket.save()

            return redirect(self.success_url)

        # If any form is invalid, re-render the page with the error messages
        return self.render_to_response(
            self.get_context_data(form=form, ticket_form=ticket_form, vip_ticket_form=vip_ticket_form)
        )


class EventDetailsView(DetailView):
    model = Event
    template_name = 'events/event_details.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase_form'] = TicketPurchaseForm()

        if self.request.user.is_authenticated:
            event = self.get_object()
            user_likes_event = Like.objects.filter(user=self.request.user, event=event).exists()
            context['user_likes_event'] = user_likes_event

        return context


@method_decorator(login_required, name='dispatch')
class EventEditView(UpdateView):
    model = Event
    form_class = EventAddForm
    template_name = 'events/event_edit.html'
    success_url = reverse_lazy('user_created_events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['ticket_form'] = TicketForm(self.request.POST, instance=self.object)
            context['vip_ticket_form'] = VipTicketForm(self.request.POST, instance=self.object)
        else:
            context['ticket_form'] = TicketForm(instance=self.object.tickets.filter(ticket_type=Ticket.REGULAR).first())
            context['vip_ticket_form'] = VipTicketForm(
                instance=self.object.tickets.filter(ticket_type=Ticket.VIP).first())

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ticket_form = context['ticket_form']
        vip_ticket_form = context['vip_ticket_form']

        if form.is_valid() and ticket_form.is_valid() and vip_ticket_form.is_valid():
            self.object = form.save()

            ticket = ticket_form.save(commit=False)
            ticket.event = self.object
            ticket.save()

            vip_ticket = vip_ticket_form.save(commit=False)
            vip_ticket.event = self.object
            vip_ticket.save()

            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form))


@login_required
def user_created_events(request):
    events_created_by_user = Event.objects.filter(creator=request.user)
    context = {'user_created_events': events_created_by_user}
    return render(request, 'accounts/user_created_events.html', context)


def events_by_category(request, category):
    category_events = Event.objects.filter(category=category)

    context = {
        'category_events': category_events,
        'selected_category': category,
    }

    return render(request, 'events/category_events.html', context)


class LocationAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return City.objects.none()

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q) | Q(country__name__istartswith=self.q))

        return qs
