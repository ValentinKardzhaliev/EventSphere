from django import forms

from .models import Event
from ..tickets.models import Ticket


# class EventAddForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = [
#             'title',
#             'description',
#             'date_and_time',
#             'venue',
#             'category',
#             'contact_information',
#             'organizer',
#             'image',
#         ]
#
#  widgets = {
#     'date_and_time': forms.DateTimeInput(
#        attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local'}),
# }
#
#     tickets = inlineformset_factory(Event, Ticket, fields=('ticket_type', 'price', 'quantity_available'), extra=1,
#                                     can_delete=False)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add any additional customization for the form fields here if needed
#
#     def clean_date_and_time(self):
#         # Additional cleaning logic for date_and_time if needed
#         return self.cleaned_data['date_and_time']

class EventAddForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_and_time', 'venue', 'category', 'contact_information', 'organizer',
                  'image']

    # Additional fields for ticket creation
    vip_quantity = forms.IntegerField(label='VIP Tickets Quantity', min_value=0, required=True)
    regular_quantity = forms.IntegerField(label='Regular Tickets Quantity', min_value=0, required=True)

    widgets = {
        'date_and_time': forms.DateTimeInput(
            attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local'}),
    }

    def save(self, commit=True):
        event = super(EventAddForm, self).save(commit)

        # Create VIP and Regular tickets for the event
        vip_quantity = self.cleaned_data.get('vip_quantity')
        regular_quantity = self.cleaned_data.get('regular_quantity')

        Ticket.objects.create(event=event, ticket_type=Ticket.VIP, quantity=vip_quantity)
        Ticket.objects.create(event=event, ticket_type=Ticket.REGULAR, quantity=regular_quantity)

        return event
