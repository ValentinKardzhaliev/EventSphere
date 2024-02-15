from django.db import models
from django.utils import timezone

from event_ticketing_system.events.models import Event
from event_ticketing_system.web_auth.models import EventAppUser


class Ticket(models.Model):
    VIP = 'VIP'
    REGULAR = 'Regular'

    TICKET_TYPE_CHOICES = [
        (VIP, 'VIP'),
        (REGULAR, 'Regular'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)
    quantity_available = models.PositiveIntegerField()
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.event.title} - {self.ticket_type} Ticket"

    class Meta:
        unique_together = ('event', 'ticket_type')


class Purchase(models.Model):
    user = models.ForeignKey(EventAppUser, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    refund_deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.ticket.event.title} - {self.quantity} tickets"

    def save(self, *args, **kwargs):
        if not self.pk:
            refund_period = timezone.timedelta(days=1)
            self.refund_deadline = timezone.now() + refund_period

        super().save(*args, **kwargs)

