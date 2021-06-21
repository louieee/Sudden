from django.contrib import admin

# Register your models here.
from tenant.models import Room, ContactInfo, Booking

admin.site.register(Room)
admin.site.register(ContactInfo)
admin.site.register(Booking)