from django.db import models


class Ticket(models.Model):
    TICKET_TYPE_CHOICES = [
        ('regular', 'Regular Ticket'),
        ('vip', 'VIP Ticket'),
    ]

    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
