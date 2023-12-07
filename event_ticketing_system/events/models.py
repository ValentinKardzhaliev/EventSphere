from django.contrib.auth import get_user_model
from django.db import models

from event_ticketing_system.web_auth.models import EventAppUser

UserModel = get_user_model()


class Event(models.Model):
    MUSIC = 'Music'
    NIGHTLIFE = 'Nightlife'
    PERFORMING_VISUAL_ARTS = 'Performing & Visual Arts'
    HOLIDAYS = 'Holidays'
    HEALTH = 'Health'
    HOBBIES = 'Hobbies'
    BUSINESS = 'Business'
    FOOD_DRINK = 'Food & Drink'

    CATEGORY_CHOICES = [
        (MUSIC, 'Music'),
        (NIGHTLIFE, 'Nightlife'),
        (PERFORMING_VISUAL_ARTS, 'Performing & Visual Arts'),
        (HOLIDAYS, 'Holidays'),
        (HEALTH, 'Health'),
        (HOBBIES, 'Hobbies'),
        (BUSINESS, 'Business'),
        (FOOD_DRINK, 'Food & Drink'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    date_and_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    organizer = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    contact_information = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.available_tickets = self.total_tickets
        super().save(*args, **kwargs)

