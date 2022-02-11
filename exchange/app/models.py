from django.db import models
from django.utils import timezone
from djongo.models.fields import ObjectIdField, Field
from django.contrib.auth.models import User
from django.conf import settings

# TODO oggetto "profitto"
class Profile(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ips = models.Field(default=[])
    subprofile = models.Field(default={})
    ip_address = models.CharField(max_length=150, blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)


class Wallet(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc_wallet = models.FloatField(default=0)
    usd_wallet = models.FloatField(default=0)
    btc_balance = models.FloatField(default=0)
    usd_balance = models.FloatField(default=0)

    def __str__(self):
        text = f"Wallet n. {self._id}. User owner: {self.user}"
        return text


class Order(models.Model):
    _id = ObjectIdField()
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=5)
    type = models.CharField(max_length=4)
    price = models.FloatField()
    quantity = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_id(self):
        return self._id