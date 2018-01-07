from django.db import models

class Train(models.Model):
    train_id     = models.AutoField(primary_key=True)
    train_number = models.CharField(max_length=6)
    from_city    = models.CharField(max_length=128)
    to_city      = models.CharField(max_length=128)
    ticket_price = models.IntegerField()
    total_places = models.IntegerField()
    free_places  = models.IntegerField()
    date         = models.CharField(max_length=10)
    time         = models.CharField(max_length=5)
    state        = models.IntegerField(default=0)