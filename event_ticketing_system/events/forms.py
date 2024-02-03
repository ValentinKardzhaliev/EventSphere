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

    vip_quantity_available = forms.IntegerField(label='VIP Tickets Quantity', min_value=0, required=True)
    vip_price = forms.DecimalField(label='VIP Ticket Price', min_value=0, required=True)
    regular_quantity_available = forms.IntegerField(label='Regular Tickets Quantity', min_value=0, required=True)
    regular_price = forms.DecimalField(label='Regular Ticket Price', min_value=0, required=True)

    class Meta:
        model = Event
        fields = '__all__'

        widgets = {
            'date_and_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventAddForm, self).__init__(*args, **kwargs)
        self.fields.pop('creator')

    def create_tickets(self, event):
        # Create VIP ticket
        Ticket.objects.create(
            event=event,
            ticket_type=Ticket.VIP,
            quantity_available=self.cleaned_data['vip_quantity_available'],
            price_per_ticket=self.cleaned_data['vip_price']
        )

        # Create Regular ticket
        Ticket.objects.create(
            event=event,
            ticket_type=Ticket.REGULAR,
            quantity_available=self.cleaned_data['regular_quantity_available'],
            price_per_ticket=self.cleaned_data['regular_price']
        )

    def save(self, commit=True):
        event = super(EventAddForm, self).save(commit=False)

        if commit:
            event.save()

        self.create_tickets(event)

        return event


class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Number of Tickets')
    ticket_type = forms.ChoiceField(choices=Ticket.TICKET_TYPE_CHOICES, label='Ticket Type')
