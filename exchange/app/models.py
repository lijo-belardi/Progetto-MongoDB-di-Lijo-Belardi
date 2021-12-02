from django.db import models
from djongo.models.fields import ObjectIdField, Field
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ips = models.Field(default=[])
    subprofile = models.Field(default={})

class Wallet(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc_wallet = models.FloatField(default=0)
    usd_wallet = models.FloatField(default=0)
    btc_balance = models.FloatField()
    usd_balance = models.FloatField()
    btc_available = models.FloatField()
    usd_available = models.FloatField()

    def __str__(self):
        text = f'Wallet n. {self._id}. User owner: {self.user}'
        return text


class OrderToSell(models.Model):
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    publish_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderToBuy(models.Model):
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    publish_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)