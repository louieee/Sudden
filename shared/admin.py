from django.contrib import admin

# Register your models here.
from shared.models import RoomType, EmailTemplate

admin.site.register(RoomType)
admin.site.register(EmailTemplate)
