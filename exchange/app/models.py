from django.db import models
from djongo.models.fields import ObjectIdField, Field
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ips = models.Field(default=[])
    subprofile = models.Field(default={})


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    quantity = models.FloatField()