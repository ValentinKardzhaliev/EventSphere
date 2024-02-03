from django.contrib import admin

from .forms import EventAddForm
from .models import Event
from ..tickets.models import Ticket


class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = [TicketInline]

    def save_model(self, request, obj, form, change):
        if not obj.creator:  # Check if creator is not set
            obj.creator = request.user  # Set the creator to the logged-in user
        super().save_model(request, obj, form, change)


admin.site.register(Event, EventAdmin)
