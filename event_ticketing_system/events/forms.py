from django import forms
from django.forms.widgets import DateTimeInput
from .models import Event
from ..tickets.models import Ticket


class EventAddForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_and_time', 'venue', 'category', 'contact_information', 'organizer',
                  'image']

        widgets = {
            'date_and_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # Additional fields for ticket creation
    vip_quantity_available = forms.IntegerField(label='VIP Tickets Quantity', min_value=0, required=True)
    vip_price = forms.DecimalField(label='VIP Ticket Price', min_value=0, required=True)
    regular_quantity_available = forms.IntegerField(label='Regular Tickets Quantity', min_value=0, required=True)
    regular_price = forms.DecimalField(label='Regular Ticket Price', min_value=0, required=True)

    def save(self, commit=True):
        event = super(EventAddForm, self).save(commit)

        # Create VIP and Regular tickets for the event
        vip_quantity_available = self.cleaned_data.get('vip_quantity_available')
        vip_price = self.cleaned_data.get('vip_price')
        regular_quantity_available = self.cleaned_data.get('regular_quantity_available')
        regular_price = self.cleaned_data.get('regular_price')

        Ticket.objects.create(event=event, ticket_type=Ticket.VIP, quantity_available=vip_quantity_available,
                              price_per_ticket=vip_price)
        Ticket.objects.create(event=event, ticket_type=Ticket.REGULAR, quantity_available=regular_quantity_available,
                              price_per_ticket=regular_price)

        return event
