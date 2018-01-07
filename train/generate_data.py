import random
from datetime import  date, time

from servise.models import Train

cities = ["Москва", "Пенза"]

train_number = "111м"
ticket_price = 1000
total_places = 20
free_places  = 20


Train.objects.all().delete()

for i in range(1, 11):
    train = {}
    train["train_number"] = train_number
    train["from_city"] = cities[i % 2]
    train["to_city"] = cities[(i+1) % 2]
    train["ticket_price"] = ticket_price
    train["total_places"] = total_places
    train["free_places"] = free_places
    train["date"] = str(date(2017, 11, 2 * i))
    train["time"] = str(time(random.randint(0, 23), random.randint(0, 59)).strftime("%H:%M"))
    Train.objects.create(**train)