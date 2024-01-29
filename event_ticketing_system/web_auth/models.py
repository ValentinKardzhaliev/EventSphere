from django.db import models
from django.contrib.auth import models as auth_models


class EventAppUser(auth_models.AbstractUser):
    email = models.EmailField(
        unique=True,
    )

    profile_picture = models.ImageField(
        upload_to='profile_images/',
        default='general_images/anon_profile_image.png',
    )

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)

        # Send email on successful register: Variant 2
        # Good enough, but there is a better option (signals)
        # send_mail....
        return result

    def __str__(self):
        return self.username
