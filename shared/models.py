from django.db import models


# Create your models here.

class RoomType(models.Model):
    name = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name


