from django.db import models

from event_ticketing_system.events.models import Event


class Ticket(models.Model):
    VIP = 'VIP'
    REGULAR = 'Regular'

    TICKET_TYPE_CHOICES = [
        (VIP, 'VIP'),
        (REGULAR, 'Regular'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.event.title} - {self.ticket_type} Ticket"

    class Meta:
        unique_together = ('event', 'ticket_type')