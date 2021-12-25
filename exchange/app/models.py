from django.db import models
from django.utils import timezone
from djongo.models.fields import ObjectIdField, Field
from django.contrib.auth.models import User
from django.conf import settings


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


class OrderToBuy(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=5)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    publish_on = models.DateTimeField(auto_now_add=True)


class OrderToSell(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=5)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    publish_on = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


