from django import forms
from event_ticketing_system.events.models import Event


class BaseEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title',
            'description',
            'date_and_time',
            'venue',
            'total_tickets',
            'ticket_price',
            'organizer',
            'image',
            'category',
            'contact_information',
        )

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title of the event'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description of the event'}),
            'date_and_time': forms.DateTimeInput(
                attrs={'placeholder': 'Date and time',
                       'format': '%Y-%m-%d %H:%M',
                       'type': 'datetime-local'}),
            'venue': forms.TextInput(attrs={'placeholder': 'Venue where the event will be held'}),
            'total_tickets': forms.NumberInput(attrs={'placeholder': 'Total number of tickets'}),
            'ticket_price': forms.NumberInput(attrs={'placeholder': 'Ticket price'}),
            'organizer': forms.TextInput(attrs={'placeholder': 'Event organizer'}),
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Event image'}),
            'category': forms.Select(attrs={'placeholder': 'Event category'}),
            'contact_information': forms.TextInput(attrs={'placeholder': 'Contact information'}),
        }

    labels = {
        'title': 'Title of the event',
        'description': 'Description of the event',
        'date_and_time': 'Date and time of the event',
        'venue': 'Venue where the event will be held',
        'total_tickets': 'Total number of tickets',
        'ticket_price': 'Ticket price',
        'organizer': 'Event organizer',
        'image': 'Event image',
        'category': 'Event category',
        'contact_information': 'Contact information',
    }


class EventAddForm(BaseEventForm):
    pass


class EventEditForm(BaseEventForm):
    pass


class EventDeleteForm(BaseEventForm):
    class Meta:
        model = Event
        fields = []

    def __init__(self, *args, **kwargs):
        super(EventDeleteForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['readonly'] = True
