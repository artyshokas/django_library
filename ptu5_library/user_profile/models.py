from django.db import models
from django.contrib.auth import get_user_model



class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name="user",
        on_delete=models.CASCADE,
        related_name="profile",
    )

    photo = models.ImageField("photo", upload_to='user_profile/photo', null=True, blank=True, )


    def __str__(self):
        return f"{self.user} profile"
