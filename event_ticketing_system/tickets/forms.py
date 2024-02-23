from django import forms
from .models import Ticket


class RegularTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'quantity_available', 'price_per_ticket']
        widgets = {
            'ticket_type': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(RegularTicketForm, self).__init__(*args, **kwargs)
        self.fields['ticket_type'].initial = Ticket.REGULAR
        self.fields['ticket_type'].widget.attrs['disabled'] = True


class VIPTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'quantity_available', 'price_per_ticket']
        widgets = {
            'ticket_type': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(VIPTicketForm, self).__init__(*args, **kwargs)
        self.fields['ticket_type'].initial = Ticket.VIP
        self.fields['ticket_type'].widget.attrs['disabled'] = True
