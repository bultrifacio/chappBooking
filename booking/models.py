import datetime, uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Room(models.Model):
    type_text = models.CharField(max_length=200)
    available_date = models.DateField()
    price_number = models.FloatField()
    description_text = models.CharField(max_length=1000)

    def __str__(self):
        return '{type} room, price:{price}'.format(type=self.type_text,price=self.price_number)


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    amount_number = models.FloatField()
    days_number = models.IntegerField()
    payment_card_text = models.CharField(max_length=20)
    phone_number_text = models.CharField(max_length=20)
    comment_text = models.CharField(max_length=1000, null=True)
    name_text = models.CharField(max_length=60)
    surname_text = models.CharField(max_length=60)
    id_card_text = models.CharField(max_length=20)
    email = models.EmailField()
    date = models.DateField()

    def __str__(self):
        return '{}'.format(self.code)
