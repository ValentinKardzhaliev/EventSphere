from django import forms
from django.forms.widgets import DateTimeInput
from .models import Event
from ..tickets.models import Ticket
from cities_light.models import City
from dal import autocomplete


class EventAddForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='location-autocomplete')
    )

    class Meta:
        model = Event
        fields = '__all__'

        widgets = {
            'date_and_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventAddForm, self).__init__(*args, **kwargs)
        self.fields.pop('creator')



class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Number of Tickets')
    ticket_type = forms.ChoiceField(choices=Ticket.TICKET_TYPE_CHOICES, label='Ticket Type')
