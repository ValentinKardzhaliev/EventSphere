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
