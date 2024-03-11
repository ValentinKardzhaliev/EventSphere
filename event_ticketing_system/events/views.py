from dal import autocomplete
from cities_light.models import City
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Event
from .forms import EventAndTicketsForm, EventEditForm
from ..common.models import Like
from ..tickets.forms import RegularTicketForm, VIPTicketForm, TicketPurchaseForm
from ..tickets.models import Ticket


@method_decorator(login_required, name='dispatch')
class EventAddView(CreateView):
    model = Event
    template_name = 'events/event_add.html'
    form_class = EventAndTicketsForm
    success_url = reverse_lazy('event_details')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)

        self.object.save()

        regular_quantity = form.cleaned_data['regular_quantity_available']

        Ticket.objects.create(event=self.object, ticket_type='Regular', quantity_available=regular_quantity,
                              price_per_ticket=form.cleaned_data['regular_price_per_ticket'])

        vip_quantity = form.cleaned_data.get('vip_quantity_available')
        vip_price = form.cleaned_data.get('vip_price_per_ticket')

        if vip_quantity is not None and vip_price is not None:
            Ticket.objects.create(
                event=self.object,
                ticket_type='VIP',
                quantity_available=vip_quantity,
                price_per_ticket=vip_price
            )
        else:
            Ticket.objects.create(
                event=self.object,
                ticket_type='VIP',
                quantity_available=0,
                price_per_ticket=0
            )

        return response

    def get_success_url(self):
        return reverse_lazy('event_details', kwargs={'pk': self.object.pk})


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
    form_class = EventEditForm
    template_name = 'events/event_edit.html'
    success_url = reverse_lazy('user_created_events')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator != self.request.user:
            raise PermissionDenied("You don't have permission to edit this event.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['ticket_form'] = RegularTicketForm(self.request.POST, instance=self.object.tickets.filter(
                ticket_type=Ticket.REGULAR).first(), prefix='regular')
            context['vip_ticket_form'] = VIPTicketForm(self.request.POST, instance=self.object.tickets.filter(
                ticket_type=Ticket.VIP).first(), prefix='vip')
        else:
            context['ticket_form'] = RegularTicketForm(
                instance=self.object.tickets.filter(ticket_type=Ticket.REGULAR).first(), prefix='regular')
            context['vip_ticket_form'] = VIPTicketForm(
                instance=self.object.tickets.filter(ticket_type=Ticket.VIP).first(), prefix='vip')

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
