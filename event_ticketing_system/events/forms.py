from django import forms
from django.forms.widgets import DateTimeInput
from .models import Event
from cities_light.models import City
from dal import autocomplete


class EventAndTicketsForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='location-autocomplete')
    )
    regular_quantity_available = forms.IntegerField(label='Regular Tickets Quantity', min_value=0)
    regular_price_per_ticket = forms.DecimalField(label='Regular Tickets Price', min_value=0)
    vip_quantity_available = forms.IntegerField(label='VIP Tickets Quantity', min_value=0, required=False)
    vip_price_per_ticket = forms.DecimalField(label='VIP Tickets Price', min_value=0, required=False)

    class Meta:
        model = Event
        exclude = ['creator']

        widgets = {
            'date_and_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class EventEditForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='location-autocomplete')
    )

    class Meta:
        model = Event
        exclude = ['creator']

        widgets = {
            'date_and_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

