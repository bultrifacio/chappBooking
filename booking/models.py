import datetime, uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Room(models.Model):
    uploadPath = '.\static\booking\images\rooms'
    type_text = models.CharField(max_length=200)
    available_date = models.DateField()
    price_number = models.FloatField()
    description_text = models.CharField(max_length=1000, default='')

    def __str__(self):
        return '{type} room for {price}'.format(type=self.type_text,price=self.price_number)

    def is_available(self):
        return self.available_date <= timezone.now()

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    days = models.IntegerField(default=1)
    payment_card = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    comment_text = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return '{}'.format(self.code)
