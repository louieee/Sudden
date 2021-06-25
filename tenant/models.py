from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

from shared.models import RoomType


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Room(models.Model):
    number = models.PositiveIntegerField(default=0)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f'Room {self.number}'


class ContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(default='', max_length=100)
    phone = models.CharField(default='', max_length=15)

    def __str__(self):
        return f'{self.user.username} contact'


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()

    def __str__(self):
        return f'{self.customer} booking for room {self.room.number}'

    def vacant(self):
        return self.time_out < timezone.now()


class Mail(models.Model):
    name = models.CharField(default='', max_length=50)

    template = models.ForeignKey('shared.EmailTemplate',
                                 on_delete=models.SET_NULL, null=True, default=None)
    subject = models.CharField(max_length=255, default='')
    sender_email = models.EmailField()
    sender_name = models.CharField(max_length=50, default='')
    recipients = models.JSONField()
    attachments = models.JSONField(blank=True)
    cc = models.JSONField(default=None, null=True, blank=True)
    bcc = models.JSONField(default=None, null=True, blank=True)
    context = models.JSONField()

    def __str__(self):
        return self.name

    def send(self):
        context = dict(self.context)
        if self.cc:
            context['cc'] = self.cc
        if self.bcc:
            context['bcc'] = self.bcc
        context['subject'] = self.subject
        context['sender_email'] = self.sender_email
        context['sender_name'] = self.sender_name
        context['recipients'] = self.recipients
        context['attachments'] = self.attachments
        if self.template is not None:
            self.template.context = context
            self.template.send()
        else:
            print('Email not sent. Template no longer exists.')
