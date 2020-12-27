from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class URLMapping(models.Model):
    id = models.IntegerField(primary_key=True)
    url_hash = models.CharField(max_length=30, unique=True, null=False)
    url = models.TextField(unique=True, null=False)

    def __str__(self):
        return f"URL {self.url[:10]}... mapped to hash {self.url_hash}."


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)