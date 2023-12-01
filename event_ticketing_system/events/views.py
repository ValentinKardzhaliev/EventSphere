from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event
from .forms import EventEditForm, EventDeleteForm


class EventAddView(CreateView):
    model = Event
    form_class = EventEditForm
    template_name = 'events/event_add.html'
    # success_url = reverse_lazy('events_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


# @login_required
class EventDetailsView(DetailView):
    model = Event
    template_name = 'events/event_details.html'
    context_object_name = 'event'


class EventEditView(UpdateView):
    model = Event
    form_class = EventEditForm
    template_name = 'events/event_edit.html'
    # success_url = reverse_lazy('events_list')


class EventDeleteView(DeleteView):
    model = Event
    form_class = EventDeleteForm
    template_name = 'events/event_delete.html'
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        """
        Override the get_object method to customize the object retrieval.
        This is needed to ensure the correct object is retrieved for deletion.
        """
        return self.model.objects.get(pk=self.kwargs['pk'])
