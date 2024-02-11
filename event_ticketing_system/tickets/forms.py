# tickets/forms.py
from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'quantity_available', 'price_per_ticket']
        widgets = {
            'price_per_ticket': forms.NumberInput(attrs={'step': '1.00', 'placeholder': 'Price per ticket in $'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the ticket_type field to be disabled and set to 'Regular'
        self.fields['ticket_type'].disabled = True
        self.initial['ticket_type'] = Ticket.REGULAR


class VipTicketForm(TicketForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the ticket_type field to be disabled and set to 'VIP'
        self.fields['ticket_type'].disabled = True
        self.initial['ticket_type'] = Ticket.VIP
