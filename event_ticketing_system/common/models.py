from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from event_ticketing_system.events.models import Event
from event_ticketing_system.web_auth.models import EventAppUser

UserModel = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.event.title}"
