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

    def __init__(self, *args, quantity_available=None, price_per_ticket=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ticket_type'].disabled = True
        self.initial['ticket_type'] = Ticket.REGULAR

        if quantity_available is not None:
            self.fields['quantity_available'].widget.attrs['value'] = quantity_available[0]
        if price_per_ticket is not None:
            self.fields['price_per_ticket'].widget.attrs['value'] = price_per_ticket[0]


class VipTicketForm(TicketForm):
    def __init__(self, *args, show_vip_fields=False, quantity_available=None, price_per_ticket=None, **kwargs):
        super().__init__(*args, quantity_available=quantity_available, price_per_ticket=price_per_ticket, **kwargs)
        self.fields['ticket_type'].disabled = True
        self.initial['ticket_type'] = Ticket.VIP
        self.show_vip_fields = show_vip_fields
        if quantity_available is not None:
            self.fields['quantity_available'].widget.attrs['value'] = quantity_available[0]
        if price_per_ticket is not None:
            self.fields['price_per_ticket'].widget.attrs['value'] = price_per_ticket[0]
