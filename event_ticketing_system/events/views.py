from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventAddForm


class EventAddView(CreateView):
    model = Event
    form_class = EventAddForm
    template_name = 'events/event_add.html'
    success_url = reverse_lazy('index')  # Adjust 'event_list' to the actual URL name for your events list

    @login_required
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventDetailsView(DetailView):
    model = Event
    template_name = 'events/event_details.html'
    context_object_name = 'event'


@login_required
def user_created_events(request):
    events_created_by_user = Event.objects.filter(creator=request.user)
    context = {'user_created_events': events_created_by_user}
    return render(request, 'events/user_created_events.html', context)
