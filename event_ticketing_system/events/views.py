from dal import autocomplete
from cities_light.models import City, Country
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventAddForm, TicketPurchaseForm


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


@login_required
def user_created_events(request):
    events_created_by_user = Event.objects.filter(creator=request.user)
    context = {'user_created_events': events_created_by_user}
    return render(request, 'events/user_created_events.html', context)


def events_by_category(request, category):
    # Filter events based on the selected category
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
