from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from event_ticketing_system.events.models import Event  # Assuming your events model is in an 'events' app

UserModel = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='likes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='likers')

    def __str__(self):
        return f"{self.user.username} likes {self.event.title}"
