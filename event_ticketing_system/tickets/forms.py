from django import forms

from .models import Ticket


class RegularTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['quantity_available', 'price_per_ticket']


class VIPTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['quantity_available', 'price_per_ticket']


class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Number of Tickets')
    ticket_type = forms.ChoiceField(choices=Ticket.TICKET_TYPE_CHOICES, label='Ticket Type')

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        if event:
            ticket_choices = [(ticket.ticket_type, f"{ticket.ticket_type} - Quantity: {ticket.quantity_available}, Price: {ticket.price_per_ticket}")
                              for ticket in event.tickets.all()]
            self.fields['ticket_type'].choices = ticket_choices
