from django import forms
from django.forms import DateTimeInput

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

    vip_quantity = forms.IntegerField(label='VIP Tickets Quantity', min_value=0, required=True)
    vip_price = forms.DecimalField(label='VIP Ticket Price', min_value=0, required=True)
    regular_quantity = forms.IntegerField(label='Regular Tickets Quantity', min_value=0, required=True)
    regular_price = forms.DecimalField(label='Regular Ticket Price', min_value=0, required=True)

    def save(self, commit=True):
        event = super(EventAddForm, self).save(commit)

        vip_quantity = self.cleaned_data.get('vip_quantity')
        vip_price = self.cleaned_data.get('vip_price')
        regular_quantity = self.cleaned_data.get('regular_quantity')
        regular_price = self.cleaned_data.get('regular_price')

        Ticket.objects.create(event=event, ticket_type=Ticket.VIP, quantity=vip_quantity, price_per_ticket=vip_price)
        Ticket.objects.create(event=event, ticket_type=Ticket.REGULAR, quantity=regular_quantity,
                              price_per_ticket=regular_price)

        return event
