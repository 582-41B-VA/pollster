from django.db import models


class Subscription(models.Model):
    name = models.CharField()
    price = models.PositiveIntegerField()
