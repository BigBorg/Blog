from django.core.urlresolvers import reverse
from accounts import serializer
from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL # it's a string...

class Account(models.Model):
    user = models.OneToOneField(User)
    email_activated = models.BooleanField(default=False)

    def get_email_activation_url(self):
        if self.user.id is None:
            return None
        email_token = serializer.dumps(self.id)
        activation_url = settings.MYHOST + reverse("accounts:activation", kwargs={"token":email_token})
        return activation_url
