from django.contrib import admin

from .models import Event
from ..tickets.models import Ticket


class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = [TicketInline]

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Event, EventAdmin)
