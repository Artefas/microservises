from django.db import models

class Billing(models.Model):
    billing_id = models.AutoField(primary_key=True)
    order_id   = models.IntegerField()
    card       = models.IntegerField()
    name       = models.CharField(max_length=32)
    state      = models.IntegerField(default=0)
    price      = models.IntegerField()