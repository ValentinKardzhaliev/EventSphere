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
