from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

from shared.models import RoomType
from utilities.python_utils import send_email


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
    is_html = models.BooleanField(default=True)
    message = models.TextField(default=None, blank=True, null=True)
    sender_email = models.EmailField()
    sender_name = models.CharField(max_length=50, default='')
    recipients = models.JSONField(default=list)
    attachments = models.JSONField(blank=True, default=list,null=True)
    cc = models.JSONField(default=list, blank=True)
    bcc = models.JSONField(default=list, blank=True)
    context = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    def send(self):
        if self.template is None and self.message not in (None, ''):
            send_email(self.sender_email, self.subject, self.recipients, self.message,
                       (self.bcc if self.bcc is not None else None),
                       (self.cc if self.cc is not None else None),
                       (self.attachments if self.attachments is not None else None), is_html=False)
        elif self.template is not None and self.message in (None, ''):
            context = dict(self.context)
            if list(self.cc).__len__() > 0:
                context['cc'] = self.cc
            if list(self.bcc).__len__() > 0:
                context['bcc'] = self.bcc
            context['subject'] = self.subject
            context['sender_email'] = self.sender_email
            context['sender_name'] = self.sender_name
            context['recipients'] = self.recipients
            context['attachments'] = self.attachments
            context['is_html'] = self.is_html
            self.template.context = context
            self.template.send()
        elif self.template is None and self.message in (None, ''):
            raise Exception('template does not exist.')
