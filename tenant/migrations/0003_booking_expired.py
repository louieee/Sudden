# Generated by Django 3.2.4 on 2021-06-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0002_alter_room_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]