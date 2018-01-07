from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user     = models.ForeignKey(User, related_name='user_orders', on_delete=models.CASCADE)
    train_id = models.IntegerField()
    ticket_count = models.IntegerField()
    state    = models.IntegerField(default=0)