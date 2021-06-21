from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from shared.models import RoomType


class Room(models.Model):
    number = models.IntegerField(default=0)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)


class ContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(default='', max_length=100)
    phone = models.CharField(default='', max_length=15)

    def __str__(self):
        return f'{self.user.username} contact'


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()

    def __str__(self):
        return f'{self.customer} booking for room {self.room.number}'

    def vacant(self):
        return self.time_out < timezone.now()